// SentinelSOC Live: Client Application Engine

document.addEventListener("DOMContentLoaded", () => {
  // Navigation Tabs
  const navButtons = document.querySelectorAll(".nav-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  navButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      navButtons.forEach(b => b.classList.remove("active"));
      tabContents.forEach(t => t.classList.remove("active"));
      
      btn.classList.add("active");
      const tabId = btn.getAttribute("data-tab");
      document.getElementById(tabId).classList.add("active");
    });
  });

  // Live Clock
  function updateClock() {
    const now = new Date();
    document.getElementById("live-clock").textContent = now.toTimeString().split(" ")[0];
  }
  setInterval(updateClock, 1000);
  updateClock();

  // Radar Canvas Setup
  const canvas = document.getElementById("radar-canvas");
  const ctx = canvas.getContext("2d");
  let radarAngle = 0;
  const radarBlips = [];

  function drawRadar() {
    const w = canvas.width;
    const h = canvas.height;
    const cx = w / 2;
    const cy = h / 2;
    const radius = Math.min(cx, cy) - 15;

    ctx.clearRect(0, 0, w, h);

    // Circles
    ctx.strokeStyle = "rgba(0, 229, 255, 0.25)";
    ctx.lineWidth = 1;
    [0.3, 0.6, 0.9].forEach(factor => {
      ctx.beginPath();
      ctx.arc(cx, cy, radius * factor, 0, Math.PI * 2);
      ctx.stroke();
    });

    // Crosshairs
    ctx.beginPath();
    ctx.moveTo(cx - radius, cy);
    ctx.lineTo(cx + radius, cy);
    ctx.moveTo(cx, cy - radius);
    ctx.lineTo(cx, cy + radius);
    ctx.stroke();

    // Sweep Line
    radarAngle += 0.035;
    const sweepX = cx + Math.cos(radarAngle) * radius;
    const sweepY = cy + Math.sin(radarAngle) * radius;

    const grad = ctx.createLinearGradient(cx, cy, sweepX, sweepY);
    grad.addColorStop(0, "rgba(0, 229, 255, 0)");
    grad.addColorStop(1, "rgba(0, 255, 102, 0.8)");

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, radius, radarAngle - 0.35, radarAngle);
    ctx.closePath();
    ctx.fill();

    // Draw Blips
    for (let i = radarBlips.length - 1; i >= 0; i--) {
      const blip = radarBlips[i];
      blip.alpha -= 0.008;
      if (blip.alpha <= 0) {
        radarBlips.splice(i, 1);
        continue;
      }
      ctx.fillStyle = blip.color.replace("1)", `${blip.alpha})`);
      ctx.beginPath();
      ctx.arc(blip.x, blip.y, blip.radius, 0, Math.PI * 2);
      ctx.fill();
    }

    requestAnimationFrame(drawRadar);
  }
  drawRadar();

  function addRadarBlip(category) {
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    const dist = 30 + Math.random() * 85;
    const ang = Math.random() * Math.PI * 2;
    
    let color = "rgba(0, 229, 255, 1)";
    if (category === "SQLi") color = "rgba(255, 0, 85, 1)";
    else if (category === "XSS") color = "rgba(0, 229, 255, 1)";
    else if (category === "Path Traversal (LFI)") color = "rgba(255, 215, 0, 1)";
    else if (category === "Command Injection") color = "rgba(168, 85, 247, 1)";
    else if (category === "Brute Force") color = "rgba(0, 255, 102, 1)";

    radarBlips.push({
      x: cx + Math.cos(ang) * dist,
      y: cy + Math.sin(ang) * dist,
      radius: 4 + Math.random() * 3,
      alpha: 1.0,
      color: color
    });
  }

  // Periodic State Sync with Python Backend
  let lastEventCount = 0;
  async function syncSOCState() {
    try {
      const res = await fetch("/api/soc/state");
      if (!res.ok) return;
      const data = await res.json();

      // Update Top Stats
      document.getElementById("stat-total-req").textContent = data.total_requests;
      document.getElementById("stat-threats-blocked").textContent = data.total_threats_blocked;
      
      const ratio = data.total_requests > 0 
        ? ((data.total_threats_blocked / data.total_requests) * 100).toFixed(1) 
        : "0.0";
      document.getElementById("stat-attack-ratio").textContent = ratio + "%";

      // Missions Count
      let compCount = 0;
      for (const k in data.missions) {
        if (data.missions[k]) compCount++;
      }
      document.getElementById("stat-missions-count").textContent = `${compCount} / 5`;

      // Update Mission Chips
      updateMissionChip("chip-sqli", data.missions.mission_sqli);
      updateMissionChip("chip-xss", data.missions.mission_xss);
      updateMissionChip("chip-bruteforce", data.missions.mission_bruteforce);
      updateMissionChip("chip-lfi", data.missions.mission_lfi);
      updateMissionChip("chip-scanner", data.missions.mission_scanner);

      // Render Attack Category Bars
      renderAttackBars(data.attack_stats, data.total_threats_blocked);

      // Render Events Table
      if (data.recent_events.length > 0) {
        renderEventsTable(data.recent_events);
        if (data.recent_events.length > lastEventCount) {
          const newEv = data.recent_events[0];
          if (newEv.threats && newEv.threats.length > 0) {
            addRadarBlip(newEv.threats[0]);
          }
          lastEventCount = data.recent_events.length;
        }
      }

      // Render Blacklist
      renderBlacklist(data.blacklisted_ips);

    } catch (err) {
      console.warn("Syncing with SOC Backend...", err);
    }
  }

  function updateMissionChip(chipId, isDone) {
    const chip = document.getElementById(chipId);
    if (!chip) return;
    if (isDone) {
      chip.textContent = "CONCLUÍDO ✅";
      chip.classList.add("done");
    } else {
      chip.textContent = "PENDENTE ⏳";
      chip.classList.remove("done");
    }
  }

  function renderAttackBars(stats, totalBlocked) {
    const container = document.getElementById("attack-bars-container");
    container.innerHTML = "";
    const maxVal = Math.max(...Object.values(stats), 1);

    for (const [name, count] of Object.entries(stats)) {
      const pct = Math.round((count / maxVal) * 100);
      const item = document.createElement("div");
      item.className = "attack-bar-item";
      item.innerHTML = `
        <div class="bar-labels">
          <span>${name}</span>
          <span class="text-cyan">${count} (${totalBlocked > 0 ? Math.round((count/totalBlocked)*100) : 0}%)</span>
        </div>
        <div class="bar-track">
          <div class="bar-fill" style="width: ${pct}%"></div>
        </div>
      `;
      container.appendChild(item);
    }
  }

  function renderEventsTable(events) {
    const tbody = document.getElementById("events-table-body");
    tbody.innerHTML = "";

    events.forEach(ev => {
      const tr = document.createElement("tr");
      const sevClass = (ev.severity || "info").toLowerCase();
      const actionClass = ev.action.includes("BLOCKED") || ev.action.includes("DROPPED") ? "blocked" : "allowed";

      tr.innerHTML = `
        <td>${ev.timestamp}</td>
        <td><strong>${ev.source_ip}</strong></td>
        <td><span class="badge-action allowed">${ev.method}</span></td>
        <td><code title="${ev.payload}">${ev.path}</code></td>
        <td><span class="badge-sev ${sevClass}">${ev.severity}</span></td>
        <td><span style="color: var(--neon-cyan)">${ev.mitre}</span></td>
        <td><span class="badge-action ${actionClass}">${ev.action}</span></td>
        <td>
          <button class="btn-quarantine-sm" onclick="handleBlacklistIP('${ev.source_ip}')">Quarentena</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }

  function renderBlacklist(ips) {
    const list = document.getElementById("blacklist-list");
    list.innerHTML = "";
    if (!ips || ips.length === 0) {
      list.innerHTML = `<li class="empty-text">Nenhum IP em quarentena</li>`;
      return;
    }
    ips.forEach(ip => {
      const li = document.createElement("li");
      li.innerHTML = `
        <span>${ip}</span>
        <button class="unblock-btn" onclick="handleUnblockIP('${ip}')" title="Desbloquear">✕</button>
      `;
      list.appendChild(li);
    });
  }

  // Blacklist Handlers
  window.handleBlacklistIP = async function(ip) {
    try {
      await fetch("/api/soc/blacklist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ip: ip, action: "add" })
      });
      syncSOCState();
    } catch (e) {
      console.error(e);
    }
  };

  window.handleUnblockIP = async function(ip) {
    try {
      await fetch("/api/soc/blacklist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ip: ip, action: "remove" })
      });
      syncSOCState();
    } catch (e) {
      console.error(e);
    }
  };

  document.getElementById("btn-block-ip").addEventListener("click", () => {
    const val = document.getElementById("manual-ip-input").value.trim();
    if (val) {
      handleBlacklistIP(val);
      document.getElementById("manual-ip-input").value = "";
    }
  });

  // Red Team Exploit Triggers
  document.querySelectorAll(".btn-fire-exploit").forEach(btn => {
    btn.addEventListener("click", async () => {
      const attackType = btn.getAttribute("data-attack");
      btn.textContent = "⏳ Enviando Payload...";
      try {
        const res = await fetch("/api/tools/simulate-attack", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ type: attackType })
        });
        const data = await res.json();
        
        btn.textContent = "✅ Disparado com Sucesso!";
        setTimeout(() => {
          btn.textContent = "⚡ Disparar Novamente";
        }, 1200);

        syncSOCState();
      } catch (err) {
        btn.textContent = "❌ Falha no Envio";
      }
    });
  });

  // Scanner Mode Toggle
  document.getElementById("scan-mode").addEventListener("change", (e) => {
    const customRow = document.getElementById("custom-ports-row");
    if (e.target.value === "custom") {
      customRow.classList.remove("hidden");
    } else {
      customRow.classList.add("hidden");
    }
  });

  // Port Scanner Execution
  document.getElementById("btn-start-scan").addEventListener("click", async () => {
    const btn = document.getElementById("btn-start-scan");
    const target = document.getElementById("scan-target").value.trim();
    const mode = document.getElementById("scan-mode").value;
    const custom = document.getElementById("scan-custom-ports").value;
    const resBox = document.getElementById("scan-results-container");
    const out = document.getElementById("scan-output");

    btn.disabled = true;
    btn.textContent = "⏳ Escaneando Portas TCP...";
    resBox.classList.remove("hidden");
    out.innerHTML = `<p style="color: var(--neon-cyan)">Conectando e enviando probes TCP para ${target}...</p>`;

    try {
      const res = await fetch("/api/tools/port-scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: target, mode: mode, custom_ports: custom })
      });
      const data = await res.json();
      
      if (data.error) {
        out.innerHTML = `<p style="color: var(--neon-alert)">${data.error}</p>`;
      } else {
        let html = `
          <div style="margin-bottom: 10px; color: var(--text-muted);">
            Alvo: <strong>${data.target_host}</strong> (${data.target_ip}) | Portas Abertas: <strong class="text-neon">${data.open_ports_count}</strong>
          </div>
          <table class="soc-table">
            <thead>
              <tr>
                <th>PORTA</th>
                <th>SERVIÇO</th>
                <th>STATUS</th>
                <th>LATÊNCIA</th>
                <th>BANNER / RESPOSTA</th>
              </tr>
            </thead>
            <tbody>
        `;
        data.ports.forEach(p => {
          const isO = p.status === "OPEN";
          html += `
            <tr>
              <td><strong>${p.port}/TCP</strong></td>
              <td>${p.service}</td>
              <td><span class="badge-action ${isO ? 'allowed' : 'blocked'}">${p.status}</span></td>
              <td>${p.latency_ms} ms</td>
              <td><code>${p.banner || "-"}</code></td>
            </tr>
          `;
        });
        html += `</tbody></table>`;
        out.innerHTML = html;
      }
    } catch (e) {
      out.innerHTML = `<p style="color: var(--neon-alert)">Erro na requisição do scanner: ${e.message}</p>`;
    } finally {
      btn.disabled = false;
      btn.textContent = "🚀 Iniciar Varredura de Portas";
      syncSOCState();
    }
  });

  // Web Audit Execution
  document.getElementById("btn-start-audit").addEventListener("click", async () => {
    const btn = document.getElementById("btn-start-audit");
    const target = document.getElementById("audit-target").value.trim();
    const resBox = document.getElementById("audit-results-container");
    const out = document.getElementById("audit-output");

    btn.disabled = true;
    btn.textContent = "⏳ Auditando Cabeçalhos HTTP...";
    resBox.classList.remove("hidden");
    out.innerHTML = `<p style="color: var(--neon-cyan)">Verificando conformidade OWASP de cabeçalhos em ${target}...</p>`;

    try {
      const res = await fetch("/api/tools/web-audit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: target })
      });
      const data = await res.json();

      if (data.error) {
        out.innerHTML = `<p style="color: var(--neon-alert)">${data.error}</p>`;
      } else {
        let html = `
          <div style="margin-bottom: 12px;">
            Banner do Servidor: <code>${data.server_banner}</code> | Pontuação de Risco: <strong class="text-alert">${data.risk_score} pts</strong>
          </div>
          <h5 style="color: var(--neon-alert); margin-bottom: 8px;">❌ Cabeçalhos de Segurança Ausentes:</h5>
        `;
        if (data.missing_headers.length === 0) {
          html += `<p class="text-neon">Todos os cabeçalhos essenciais estão configurados!</p>`;
        } else {
          data.missing_headers.forEach(h => {
            html += `
              <div style="margin-bottom: 8px; padding: 6px 10px; background: rgba(255,0,85,0.08); border-left: 3px solid var(--neon-alert); border-radius: 4px;">
                <strong>${h.header}</strong> [Risco: ${h.risk}]<br>
                <span style="font-size: 0.76rem; color: var(--text-muted);">${h.impact}</span>
              </div>
            `;
          });
        }
        out.innerHTML = html;
      }
    } catch (e) {
      out.innerHTML = `<p style="color: var(--neon-alert)">Erro ao auditar alvo web: ${e.message}</p>`;
    } finally {
      btn.disabled = false;
      btn.textContent = "🔬 Analisar Cabeçalhos de Segurança";
    }
  });

  // Clear Feed
  document.getElementById("btn-clear-feed").addEventListener("click", () => {
    document.getElementById("events-table-body").innerHTML = `
      <tr><td colspan="8" class="empty-state">Visualização limpa pelo operador. Novos eventos surgirão automaticamente.</td></tr>
    `;
  });

  // Initial Sync & Loop
  syncSOCState();
  setInterval(syncSOCState, 1500);
});
