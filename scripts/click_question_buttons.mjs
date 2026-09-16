#!/usr/bin/env node
/**
 * Drive Chrome to click the six question buttons and print on-screen hits as JSON.
 */
import { execFileSync, spawn } from "node:child_process";
import { existsSync, mkdtempSync } from "node:fs";
import http from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";

const SEEDS = ["data product", "application component"];
const BUTTONS = ["qDepends", "qDependsOn", "qImpactQ", "qOwns", "qPolicies", "qTeams"];

function which(cmd) {
  try {
    return execFileSync("which", [cmd], { encoding: "utf8" }).trim();
  } catch {
    return "";
  }
}

function resolveChrome() {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) {
    return process.env.CHROME_PATH;
  }
  for (const cand of [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ]) {
    if (existsSync(cand)) return cand;
  }
  for (const cmd of ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"]) {
    const found = which(cmd);
    if (found) return found;
  }
  return process.env.CHROME_PATH || "google-chrome";
}

function getJson(url) {
  return new Promise((resolve, reject) => {
    http
      .get(url, (res) => {
        let body = "";
        res.on("data", (chunk) => {
          body += chunk;
        });
        res.on("end", () => resolve(JSON.parse(body)));
      })
      .on("error", reject);
  });
}

function waitForDevtools(child, timeoutMs = 20000) {
  return new Promise((resolve, reject) => {
    let text = "";
    const timer = setTimeout(() => {
      reject(new Error(`Chrome did not expose DevTools.\n${text}`));
    }, timeoutMs);
    const onData = (chunk) => {
      text += String(chunk);
      const match = text.match(/DevTools listening on (ws:\/\/\S+)/);
      if (match) {
        clearTimeout(timer);
        child.stderr.off("data", onData);
        resolve(match[1]);
      }
    };
    child.stderr.on("data", onData);
    child.on("error", (err) => {
      clearTimeout(timer);
      reject(
        new Error(
          `CHROME not found (${err.message}). Install Chrome or set CHROME_PATH.`,
        ),
      );
    });
    child.on("exit", (code) => {
      if (!text.includes("DevTools listening")) {
        clearTimeout(timer);
        reject(new Error(`Chrome exited ${code} before DevTools was ready.\n${text}`));
      }
    });
  });
}

function bindCdp(ws) {
  let nextId = 1;
  const pending = new Map();
  ws.addEventListener("message", (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result);
    }
  });
  return (method, params = {}, sessionId) => {
    const id = nextId++;
    return new Promise((resolve, reject) => {
      pending.set(id, { resolve, reject });
      const payload = { id, method, params };
      if (sessionId) payload.sessionId = sessionId;
      ws.send(JSON.stringify(payload));
    });
  };
}

async function evaluate(send, expression, sessionId) {
  const result = await send(
    "Runtime.evaluate",
    { expression, awaitPromise: true, returnByValue: true },
    sessionId,
  );
  if (result.exceptionDetails) {
    throw new Error(
      result.exceptionDetails.exception?.description || result.exceptionDetails.text,
    );
  }
  return result.result.value;
}

async function main() {
  const pageUrl = process.argv[2];
  if (!pageUrl) {
    console.error("usage: node scripts/click_question_buttons.mjs <index-url>");
    process.exit(2);
  }

  const bin = resolveChrome();
  const profile = mkdtempSync(join(tmpdir(), "c5-chrome-"));
  const child = spawn(
    bin,
    [
      "--headless=new",
      "--disable-gpu",
      "--no-first-run",
      "--no-default-browser-check",
      "--disable-extensions",
      "--no-sandbox",
      `--user-data-dir=${profile}`,
      "--remote-debugging-port=0",
      "about:blank",
    ],
    { stdio: ["ignore", "ignore", "pipe"] },
  );

  try {
    const browserWs = await waitForDevtools(child);
    const dbgHost = new URL(browserWs).host;
    const version = await getJson(`http://${dbgHost}/json/version`);
    const ws = new WebSocket(version.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => {
      ws.addEventListener("open", resolve, { once: true });
      ws.addEventListener("error", () => reject(new Error("CDP websocket failed")), {
        once: true,
      });
    });
    const send = bindCdp(ws);
    const created = await send("Target.createTarget", { url: pageUrl });
    const attached = await send("Target.attachToTarget", {
      targetId: created.targetId,
      flatten: true,
    });
    const sessionId = attached.sessionId;
    await send("Runtime.enable", {}, sessionId);
    await send("Page.enable", {}, sessionId);
    await evaluate(
      send,
      `new Promise((resolve, reject) => {
        const started = Date.now();
        const tick = () => {
          const n = document.getElementById("sn")?.textContent;
          const sel = document.getElementById("pathSource");
          if (n && Number(n) > 0 && sel && sel.options.length > 1) return resolve(true);
          if (Date.now() - started > 20000) {
            return reject(new Error(
              "viewer did not boot: " + (document.body?.innerText || "").slice(0, 400)
            ));
          }
          setTimeout(tick, 100);
        };
        tick();
      })`,
      sessionId,
    );

    const report = {};
    for (const seed of SEEDS) {
      report[seed] = {};
      for (const button of BUTTONS) {
        report[seed][button] = await evaluate(
          send,
          `(() => {
            const seed = ${JSON.stringify(seed)};
            const button = ${JSON.stringify(button)};
            document.getElementById("pathSource").value = seed;
            document.getElementById(button).click();
            const box = document.getElementById("pathResult");
            const text = box.innerText;
            const hits = [...box.querySelectorAll(".item b")].map((el) => el.textContent);
            return {
              title: box.querySelector("b")?.textContent || "",
              empty: text.includes("No path found"),
              hits,
              text,
            };
          })()`,
          sessionId,
        );
      }
    }
    ws.close();
    process.stdout.write(`${JSON.stringify(report)}\n`);
  } finally {
    if (!child.killed) child.kill("SIGKILL");
  }
}

main().catch((err) => {
  console.error(err && err.message ? err.message : err);
  process.exit(1);
});
