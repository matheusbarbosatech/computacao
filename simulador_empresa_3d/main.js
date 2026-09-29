// ==========================================================================
// CYBERDEFENSE 3D — MOTOR PRINCIPAL (THREE.JS POV WORK SIMULATOR)
// ==========================================================================

let scene, camera, renderer;
let clock, delta;
let currentSeconds = 8 * 3600; // 08:00:00
let timeMultiplier = 1;
let isPointerLocked = false;
let isSittingAtDesk = false;
let coffeeLevel = 100;
let reputationLevel = 80;

// Movement state
const moveState = { forward: false, backward: false, left: false, right: false };
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();
const PLAYER_SPEED = 5.5;

// Raycaster & Interactivity
let raycaster;
const mouseCenter = new THREE.Vector2(0, 0);
const interactableObjects = [];
let currentLookedObject = null;

// Audio Synthesizer (Zero external dependencies)
let audioCtx;
function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function playTone(freq, type, duration, vol = 0.1) {
    if (!audioCtx) return;
    try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(vol, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch (e) {}
}

function sfxClick() { playTone(500, 'triangle', 0.05, 0.08); }
function sfxSiren() { playTone(880, 'sawtooth', 0.2, 0.15); setTimeout(() => playTone(440, 'sawtooth', 0.3, 0.15), 180); }
function sfxCoffee() { playTone(300, 'sine', 0.1, 0.1); setTimeout(() => playTone(400, 'sine', 0.15, 0.1), 100); }
function sfxPhoneRing() { playTone(950, 'sine', 0.15, 0.12); setTimeout(() => playTone(800, 'sine', 0.2, 0.12), 150); }

// UI Elements
const crosshairEl = document.getElementById("crosshair");
const promptEl = document.getElementById("interaction-prompt");
const workstationOverlay = document.getElementById("workstation-overlay");
const controlsOverlay = document.getElementById("controlsOverlay");
const btnStartGame = document.getElementById("btnStartGame");
const btnLeaveDesk = document.getElementById("btnLeaveDesk");
const clockDisplay = document.getElementById("clockDisplay");
const coffeeBar = document.getElementById("coffeeBar");
const repBar = document.getElementById("repBar");
const phoneBanner = document.getElementById("phone-banner");
const phoneCaller = document.getElementById("phoneCaller");
const btnAnswerPhone = document.getElementById("btnAnswerPhone");
const npcDialogueBox = document.getElementById("npc-dialogue-box");
const dialogueAvatar = document.getElementById("dialogueAvatar");
const dialogueName = document.getElementById("dialogueName");
const dialogueRole = document.getElementById("dialogueRole");
const dialogueText = document.getElementById("dialogueText");
const dialogueChoices = document.getElementById("dialogueChoices");
const btnCloseDialogue = document.getElementById("btnCloseDialogue");

// 3D Meshes References
let serverLeds = [];
let deskPhoneMesh;
let coffeeCupMesh;
let monitorScreens = [];

// INITIALIZE 3D WORLD
function init() {
    const container = document.getElementById("canvas-container");

    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x060910);
    scene.fog = new THREE.FogExp2(0x060910, 0.035);

    // Camera (Player POV at 1.7m eye level)
    camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.set(0, 1.7, 4.5);
    camera.rotation.order = 'YXZ';

    // Clock
    clock = new THREE.Clock();

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Raycaster
    raycaster = new THREE.Raycaster();
    raycaster.far = 3.5;

    // Lighting
    setupLighting();

    // Build Office Environment
    buildOfficeRoom();

    // Build Workstation Desk, Dual Monitors & Accessories
    buildWorkstation();

    // Build Server Datacenter Rack
    buildServerRack();

    // Build 3D NPCs (Coworkers)
    buildNPCs();

    // Event Listeners (Controls, Resize)
    setupEventListeners();

    // Start SIEM & Incident Systems
    renderSiemList();
    renderChatHistory("soc-geral");

    // Animation Loop
    animate();
}

// LIGHTING SETUP
function setupLighting() {
    const ambientLight = new THREE.AmbientLight(0x1a2639, 0.9);
    scene.add(ambientLight);

    // Overhead Ceiling Panel Lights
    const ceilingLight1 = new THREE.PointLight(0x00d2ff, 1.4, 18);
    ceilingLight1.position.set(0, 3.8, 0);
    ceilingLight1.castShadow = true;
    scene.add(ceilingLight1);

    const ceilingLight2 = new THREE.PointLight(0x38bdf8, 1.0, 15);
    ceilingLight2.position.set(-4, 3.8, -3);
    scene.add(ceilingLight2);

    // Neon Accent Light on Server Rack
    const rackGlow = new THREE.PointLight(0x00ff88, 1.2, 8);
    rackGlow.position.set(5.5, 2, -4);
    scene.add(rackGlow);
}

// BUILD ROOM & WALLS
function buildOfficeRoom() {
    // Floor (Dark grid corporate tiles)
    const floorGeo = new THREE.PlaneGeometry(16, 16);
    const floorMat = new THREE.MeshStandardMaterial({
        color: 0x0a0f1d,
        roughness: 0.2,
        metalness: 0.5
    });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    // Floor Grid Helper
    const grid = new THREE.GridHelper(16, 32, 0x00d2ff, 0x111c33);
    grid.position.y = 0.01;
    scene.add(grid);

    // Walls Material
    const wallMat = new THREE.MeshStandardMaterial({ color: 0x0e1424, roughness: 0.8 });

    // Back Wall
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(16, 4.5, 0.4), wallMat);
    backWall.position.set(0, 2.25, -8);
    backWall.receiveShadow = true;
    scene.add(backWall);

    // Front Wall (with glass entrance)
    const frontWall = new THREE.Mesh(new THREE.BoxGeometry(16, 4.5, 0.4), wallMat);
    frontWall.position.set(0, 2.25, 8);
    scene.add(frontWall);

    // Left Wall (Windows to Night City)
    const leftWall = new THREE.Mesh(new THREE.BoxGeometry(0.4, 4.5, 16), wallMat);
    leftWall.position.set(-8, 2.25, 0);
    scene.add(leftWall);

    // Right Wall (Server room divider)
    const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.4, 4.5, 16), wallMat);
    rightWall.position.set(8, 2.25, 0);
    scene.add(rightWall);

    // Ceiling
    const ceiling = new THREE.Mesh(new THREE.PlaneGeometry(16, 16), new THREE.MeshBasicMaterial({ color: 0x05070e }));
    ceiling.position.y = 4.2;
    ceiling.rotation.x = Math.PI / 2;
    scene.add(ceiling);

    // Neon Wall Logo ("CYBERDEFENSE CORP")
    const canvasLogo = document.createElement("canvas");
    canvasLogo.width = 512;
    canvasLogo.height = 128;
    const ctx = canvasLogo.getContext("2d");
    ctx.fillStyle = "#0e1424";
    ctx.fillRect(0, 0, 512, 128);
    ctx.fillStyle = "#00d2ff";
    ctx.font = "bold 34px sans-serif";
    ctx.fillText("CYBERDEFENSE CORP", 40, 55);
    ctx.fillStyle = "#00ff88";
    ctx.font = "20px monospace";
    ctx.fillText("● GLOBAL SOC OPERATIONS", 40, 95);

    const logoTexture = new THREE.CanvasTexture(canvasLogo);
    const logoMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(5, 1.25),
        new THREE.MeshBasicMaterial({ map: logoTexture })
    );
    logoMesh.position.set(0, 3.2, -7.78);
    scene.add(logoMesh);
}

// BUILD WORKSTATION (DESK, DUAL MONITORS, PHONE, COFFEE)
function buildWorkstation() {
    const deskGroup = new THREE.Group();
    deskGroup.position.set(0, 0, 0);

    // Desk Top
    const deskTop = new THREE.Mesh(
        new THREE.BoxGeometry(2.4, 0.08, 1.2),
        new THREE.MeshStandardMaterial({ color: 0x161e31, roughness: 0.3, metalness: 0.4 })
    );
    deskTop.position.set(0, 0.75, 0);
    deskTop.castShadow = true;
    deskTop.receiveShadow = true;
    deskGroup.add(deskTop);

    // Desk Legs
    const legGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.75);
    const legMat = new THREE.MeshStandardMaterial({ color: 0x0a0f1d, metalness: 0.8 });
    const p1 = new THREE.Mesh(legGeo, legMat); p1.position.set(-1.1, 0.375, -0.5); deskGroup.add(p1);
    const p2 = new THREE.Mesh(legGeo, legMat); p2.position.set(1.1, 0.375, -0.5); deskGroup.add(p2);
    const p3 = new THREE.Mesh(legGeo, legMat); p3.position.set(-1.1, 0.375, 0.5); deskGroup.add(p3);
    const p4 = new THREE.Mesh(legGeo, legMat); p4.position.set(1.1, 0.375, 0.5); deskGroup.add(p4);

    // Gaming / Ergonomic Chair
    const chairGroup = new THREE.Group();
    chairGroup.position.set(0, 0, 0.85);
    const seat = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.08, 0.55), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.6 }));
    seat.position.y = 0.45;
    chairGroup.add(seat);
    const backrest = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.7, 0.08), new THREE.MeshStandardMaterial({ color: 0x00d2ff, roughness: 0.4 }));
    backrest.position.set(0, 0.82, 0.24);
    chairGroup.add(backrest);
    deskGroup.add(chairGroup);

    // Dual Monitors Setup
    // Monitor 1 (Left - SIEM & Alertas)
    const mon1 = createMonitor("SIEM MONITOR", -0.45, 0.8, -0.25, 0.15);
    deskGroup.add(mon1);

    // Monitor 2 (Right - CorpChat & Terminal)
    const mon2 = createMonitor("CHAT MONITOR", 0.45, 0.8, -0.25, -0.15);
    deskGroup.add(mon2);

    // Mechanical Keyboard & Mouse
    const kb = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.02, 0.15), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.5 }));
    kb.position.set(0, 0.8, 0.15);
    deskGroup.add(kb);

    const mouse = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.02, 0.1), new THREE.MeshStandardMaterial({ color: 0x00d2ff }));
    mouse.position.set(0.32, 0.8, 0.15);
    deskGroup.add(mouse);

    // Desk Telephone
    const phoneBase = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.05, 0.2), new THREE.MeshStandardMaterial({ color: 0x1e293b }));
    phoneBase.position.set(-0.85, 0.81, 0.15);
    deskPhoneMesh = phoneBase;
    deskPhoneMesh.name = "deskPhone";
    deskPhoneMesh.userData = {
        tipo: "phone",
        prompt: "[E] Atender Telefone do Ramal",
        interact: atenderTelefone
    };
    interactableObjects.push(deskPhoneMesh);
    deskGroup.add(phoneBase);

    // Coffee Mug
    const mugGeo = new THREE.CylinderGeometry(0.05, 0.045, 0.12, 16);
    const mugMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });
    coffeeCupMesh = new THREE.Mesh(mugGeo, mugMat);
    coffeeCupMesh.position.set(0.85, 0.85, 0.15);
    coffeeCupMesh.name = "coffeeCup";
    coffeeCupMesh.userData = {
        tipo: "coffee",
        prompt: "[E] Beber Café (+Energia)",
        interact: beberCafe
    };
    interactableObjects.push(coffeeCupMesh);
    deskGroup.add(coffeeCupMesh);

    scene.add(deskGroup);
}

// HELPER: CREATE 3D MONITOR WITH GLOWING CANVASES
function createMonitor(label, x, y, z, rotY) {
    const monGroup = new THREE.Group();
    monGroup.position.set(x, y, z);
    monGroup.rotation.y = rotY;

    // Bezel & Frame
    const bezel = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.44, 0.03), new THREE.MeshStandardMaterial({ color: 0x0a0f1d, metalness: 0.8 }));
    bezel.position.y = 0.22;
    monGroup.add(bezel);

    // Stand
    const stand = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.25), new THREE.MeshStandardMaterial({ color: 0x1e293b }));
    stand.position.set(0, 0.08, -0.05);
    monGroup.add(stand);

    // Screen with dynamic texture
    const canvas = document.createElement("canvas");
    canvas.width = 512;
    canvas.height = 320;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "#040711";
    ctx.fillRect(0, 0, 512, 320);
    ctx.fillStyle = "#00d2ff";
    ctx.font = "bold 24px monospace";
    ctx.fillText(`LIVE SOC: ${label}`, 30, 45);
    ctx.fillStyle = "#00ff88";
    ctx.font = "16px monospace";
    ctx.fillText("● MONITORANDO REDE CORPORATIVA", 30, 80);
    ctx.fillText("● WAZUH SIEM: ONLINE", 30, 110);
    ctx.fillText("● SURICATA IDS: ATIVO", 30, 140);
    ctx.strokeStyle = "#00d2ff";
    ctx.strokeRect(30, 170, 452, 120);
    ctx.fillStyle = "rgba(0, 210, 255, 0.2)";
    ctx.fillRect(30, 170, 452, 120);
    ctx.fillStyle = "#ffffff";
    ctx.font = "18px sans-serif";
    ctx.fillText("CLIQUE OU APERTE [E] PARA OPERAR", 65, 235);

    const screenTex = new THREE.CanvasTexture(canvas);
    const screenMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(0.66, 0.4),
        new THREE.MeshBasicMaterial({ map: screenTex })
    );
    screenMesh.position.set(0, 0.22, 0.016);
    screenMesh.name = "workstationMonitor";
    screenMesh.userData = {
        tipo: "monitor",
        prompt: "[E] Sentar na Cadeira & Operar Computador",
        interact: abrirWorkstation
    };
    interactableObjects.push(screenMesh);
    monGroup.add(screenMesh);

    monitorScreens.push(screenMesh);
    return monGroup;
}

// BUILD SERVER RACK IN CORNER
function buildServerRack() {
    const rackGroup = new THREE.Group();
    rackGroup.position.set(6, 0, -4);

    // Outer Cabinet
    const rackCabinet = new THREE.Mesh(
        new THREE.BoxGeometry(1.2, 3.2, 1.2),
        new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.7, roughness: 0.3 })
    );
    rackCabinet.position.y = 1.6;
    rackCabinet.castShadow = true;
    rackGroup.add(rackCabinet);

    // Front Glass Door
    const glass = new THREE.Mesh(
        new THREE.PlaneGeometry(1.0, 3.0),
        new THREE.MeshPhysicalMaterial({ color: 0x00d2ff, transparent: true, opacity: 0.3, transmission: 0.7 })
    );
    glass.position.set(0, 1.6, 0.61);
    rackGroup.add(glass);

    // Blinking Activity LEDs
    for (let i = 0; i < 18; i++) {
        const led = new THREE.Mesh(
            new THREE.BoxGeometry(0.04, 0.02, 0.02),
            new THREE.MeshBasicMaterial({ color: i % 2 === 0 ? 0x00ff88 : 0x00d2ff })
        );
        led.position.set(-0.35 + (i % 6) * 0.14, 0.6 + Math.floor(i / 6) * 0.7, 0.59);
        rackGroup.add(led);
        serverLeds.push(led);
    }

    // Interactivity
    const hitBox = new THREE.Mesh(new THREE.BoxGeometry(1.4, 3.4, 1.4), new THREE.MeshBasicMaterial({ visible: false }));
    hitBox.position.y = 1.6;
    hitBox.name = "serverRack";
    hitBox.userData = {
        tipo: "datacenter",
        prompt: "[E] Inspecionar Datacenter & Servidores",
        interact: () => {
            sfxClick();
            falarVozNpc("Datacenter corporativo operando com 42 nós virtuais. Sem falha de hardware.");
            alert("🛡️ DATACENTER CORPORATIVO\n\nRack 01 - Dell PowerEdge R750\nStatus: 100% UP\nBanda de Borda: 10 Gbps Fibra MikroTik CCR2004\nArmazenamento: 120 TB em RAID 10");
        }
    };
    interactableObjects.push(hitBox);
    rackGroup.add(hitBox);

    scene.add(rackGroup);
}

// BUILD 3D COWORKER NPCS (HUMANOID AVATARS IN OFFICE)
function buildNPCs() {
    // 1. Marcos (CISO - in the management desk)
    createHumanoidNPC("ciso", "Marcos (CISO)", 0x1e3a8a, -4.5, 0, -2, 0.8);

    // 2. Ricardo (Senior N3 - at the side desk)
    createHumanoidNPC("senior", "Ricardo (N3)", 0x065f46, -3, 0, 1.5, -1.2);

    // 3. Lucas (Intern - near the printer)
    createHumanoidNPC("intern", "Lucas (Estagiário)", 0x854d0e, 3.5, 0, 2, -2.5);
}

function createHumanoidNPC(id, nome, colorHex, x, y, z, rotY) {
    const npcGroup = new THREE.Group();
    npcGroup.position.set(x, y, z);
    npcGroup.rotation.y = rotY;

    // Body
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.28, 0.85, 12), new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.5 }));
    body.position.y = 0.95;
    body.castShadow = true;
    npcGroup.add(body);

    // Head
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 16), new THREE.MeshStandardMaterial({ color: 0xfbd38d, roughness: 0.7 }));
    head.position.y = 1.55;
    head.castShadow = true;
    npcGroup.add(head);

    // ID Badge / Name Tag
    const canvasName = document.createElement("canvas");
    canvasName.width = 256; canvasName.height = 64;
    const ctx = canvasName.getContext("2d");
    ctx.fillStyle = "rgba(10, 15, 26, 0.85)";
    ctx.fillRect(0, 0, 256, 64);
    ctx.strokeStyle = "#00d2ff";
    ctx.strokeRect(2, 2, 252, 60);
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 20px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(nome, 128, 40);

    const tagTex = new THREE.CanvasTexture(canvasName);
    const tagMesh = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.2), new THREE.MeshBasicMaterial({ map: tagTex, transparent: true }));
    tagMesh.position.set(0, 1.88, 0);
    npcGroup.add(tagMesh);

    // Interaction Hitbox
    const hitBox = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 1.8), new THREE.MeshBasicMaterial({ visible: false }));
    hitBox.position.y = 0.9;
    hitBox.name = `npc_${id}`;
    hitBox.userData = {
        tipo: "npc",
        npcId: id,
        prompt: `[E] Conversar com ${nome}`,
        interact: () => abrirDialogoNpc(id)
    };
    interactableObjects.push(hitBox);
    npcGroup.add(hitBox);

    scene.add(npcGroup);
}

// CONTROLS & INTERACTION LISTENERS
function setupEventListeners() {
    window.addEventListener("resize", onWindowResize);

    // Keyboard
    document.addEventListener("keydown", (e) => {
        if (isSittingAtDesk) {
            if (e.key === "Escape") fecharWorkstation();
            return;
        }

        switch (e.code) {
            case "KeyW": case "ArrowUp": moveState.forward = true; break;
            case "KeyS": case "ArrowDown": moveState.backward = true; break;
            case "KeyA": case "ArrowLeft": moveState.left = true; break;
            case "KeyD": case "ArrowRight": moveState.right = true; break;
            case "KeyE": case "Space":
                if (currentLookedObject && currentLookedObject.userData.interact) {
                    currentLookedObject.userData.interact();
                }
                break;
            case "KeyF":
                if (!phoneBanner.classList.contains("phone-hidden")) atenderTelefone();
                break;
        }
    });

    document.addEventListener("keyup", (e) => {
        switch (e.code) {
            case "KeyW": case "ArrowUp": moveState.forward = false; break;
            case "KeyS": case "ArrowDown": moveState.backward = false; break;
            case "KeyA": case "ArrowLeft": moveState.left = false; break;
            case "KeyD": case "ArrowRight": moveState.right = false; break;
        }
    });

    // PointerLock (Mouse Look)
    document.addEventListener("pointerlockchange", () => {
        isPointerLocked = (document.pointerLockElement === document.body);
        if (!isPointerLocked && !isSittingAtDesk) {
            // Optional pause or un-lock
        }
    });

    document.addEventListener("mousemove", (e) => {
        if (!isPointerLocked || isSittingAtDesk) return;
        const movementX = e.movementX || 0;
        const movementY = e.movementY || 0;

        camera.rotation.y -= movementX * 0.0022;
        camera.rotation.x -= movementY * 0.0022;
        camera.rotation.x = Math.max(-Math.PI / 2.3, Math.min(Math.PI / 2.3, camera.rotation.x));
    });

    // Click to start / Lock pointer
    btnStartGame.addEventListener("click", () => {
        initAudio();
        controlsOverlay.style.display = "none";
        document.body.requestPointerLock();
    });

    btnLeaveDesk.addEventListener("click", fecharWorkstation);
    btnAnswerPhone.addEventListener("click", atenderTelefone);
    btnCloseDialogue.addEventListener("click", fecharDialogoNpc);

    // HUD Buttons
    document.getElementById("btnToggleHelp").addEventListener("click", () => {
        controlsOverlay.style.display = "flex";
        document.exitPointerLock();
    });

    document.getElementById("btnToggleTime").addEventListener("click", () => {
        timeMultiplier = (timeMultiplier === 1) ? 5 : 1;
        document.getElementById("btnToggleTime").innerText = `⏩ ${timeMultiplier}x`;
    });

    // Monitor Tabs
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            sfxClick();
            document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            btn.classList.add("active");
            document.getElementById(btn.dataset.tab).classList.add("active");
        });
    });

    // Chat Channel Selectors
    document.querySelectorAll(".chat-channel, .chat-dm").forEach(el => {
        el.addEventListener("click", () => {
            sfxClick();
            document.querySelectorAll(".chat-channel, .chat-dm").forEach(e => e.classList.remove("active"));
            el.classList.add("active");
            const target = el.dataset.channel || el.dataset.npc;
            renderChatHistory(target);
        });
    });

    // Send Chat
    document.getElementById("btnSendChat").addEventListener("click", enviarMensagemChat);
    document.getElementById("chatInput").addEventListener("keypress", (e) => {
        if (e.key === "Enter") enviarMensagemChat();
    });

    // Terminal Input
    const termInput = document.getElementById("termInput");
    termInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            const cmd = termInput.value;
            termInput.value = "";
            execTerminal(cmd);
        }
    });

    // Mobile Virtual Joystick Setup
    setupMobileControls();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// ACTIONS / INTERACTIONS
function abrirWorkstation() {
    sfxClick();
    isSittingAtDesk = true;
    document.exitPointerLock();
    workstationOverlay.classList.remove("workstation-hidden");
}

function fecharWorkstation() {
    sfxClick();
    isSittingAtDesk = false;
    workstationOverlay.classList.add("workstation-hidden");
    document.body.requestPointerLock();
}

function beberCafe() {
    sfxCoffee();
    coffeeLevel = Math.min(100, coffeeLevel + 35);
    coffeeBar.style.width = `${coffeeLevel}%`;
    falarVozNpc("Café fresco! Energia e foco restaurados.");
}

function atenderTelefone() {
    sfxClick();
    phoneBanner.classList.add("phone-hidden");
    abrirDialogoNpc("finance");
}

function dispararChamadaTelefone(npcId, mensagem) {
    sfxPhoneRing();
    phoneCaller.innerText = mensagem;
    phoneBanner.classList.remove("phone-hidden");
}

// IN-PERSON NPC DIALOGUE
function abrirDialogoNpc(npcId) {
    sfxClick();
    document.exitPointerLock();
    const npc = NPCS[npcId];
    if (!npc) return;

    dialogueAvatar.innerText = npc.avatar;
    dialogueName.innerText = npc.nome;
    dialogueRole.innerText = npc.cargo;

    const dialogo = npc.dialogo3d.inicial;
    dialogueText.innerText = `"${dialogo.fala}"`;
    falarVozNpc(dialogo.fala, npc.vozPitch);

    dialogueChoices.innerHTML = "";
    dialogo.opcoes.forEach(op => {
        const btn = document.createElement("button");
        btn.className = "btn-choice";
        btn.innerText = `👉 ${op.texto}`;
        btn.addEventListener("click", () => {
            sfxClick();
            reputationLevel = Math.max(0, Math.min(100, reputationLevel + op.rep));
            repBar.style.width = `${reputationLevel}%`;
            dialogueText.innerText = `"${op.resposta}"`;
            falarVozNpc(op.resposta, npc.vozPitch);
            dialogueChoices.innerHTML = "";
        });
        dialogueChoices.appendChild(btn);
    });

    npcDialogueBox.classList.remove("dialogue-hidden");
}

function fecharDialogoNpc() {
    sfxClick();
    npcDialogueBox.classList.add("dialogue-hidden");
    if (!isSittingAtDesk) document.body.requestPointerLock();
}

// SIEM WORKSTATION RENDERER
function renderSiemList() {
    const list = document.getElementById("siemIncidentList");
    list.innerHTML = "";
    INCIDENT_QUEUE.forEach((inc, idx) => {
        const card = document.createElement("div");
        card.className = `siem-card ${inc.resolvido ? "resolved" : ""}`;
        card.innerHTML = `
            <div class="siem-card-top">
                <span class="siem-id">${inc.id} • ${inc.horaDisparo}</span>
                <span class="siem-sev-${inc.severidade}">${inc.severidade.toUpperCase()}</span>
            </div>
            <div class="siem-card-title">${inc.titulo}</div>
        `;
        card.addEventListener("click", () => {
            sfxClick();
            document.querySelectorAll(".siem-card").forEach(c => c.classList.remove("active"));
            card.classList.add("active");
            renderSiemDetail(inc);
        });
        list.appendChild(card);
    });
}

function renderSiemDetail(inc) {
    const detail = document.getElementById("siemDetailView");
    detail.innerHTML = `
        <div class="detail-header">
            <h3>${inc.titulo}</h3>
            <div class="detail-meta">
                <span><strong>Horário:</strong> ${inc.horaDisparo}</span>
                <span><strong>Setor:</strong> ${inc.setor}</span>
                <span><strong>Origem:</strong> ${inc.origem}</span>
            </div>
        </div>
        <p style="margin-bottom:14px; color:#cbd5e1; font-size:13px;">${inc.descricao}</p>
        <div class="log-box">${inc.log}</div>
        <div class="detail-actions">
            <h4>🛡️ PLANO DE CONTENÇÃO & RESPOSTA:</h4>
            <p style="font-size:12px; color:#8892b0; margin-bottom:12px;">Tática MITRE ATT&CK mapeada: <strong>${inc.mitre}</strong></p>
            <button class="btn-mitigate" id="btnMitigateAction">${inc.resolvido ? "✅ INCIDENTE RESOLVIDO" : "⚡ APLICAR MITIGAÇÃO CORPORATIVA"}</button>
        </div>
    `;

    document.getElementById("btnMitigateAction").addEventListener("click", () => {
        if (!inc.resolvido) {
            inc.resolvido = true;
            sfxClick();
            reputationLevel = Math.min(100, reputationLevel + 10);
            repBar.style.width = `${reputationLevel}%`;
            falarVozNpc(`Incidente ${inc.id} mitigado com sucesso.`);
            renderSiemList();
            renderSiemDetail(inc);
        }
    });
}

// CORPCAT / SLACK SYSTEM
function renderChatHistory(target) {
    const msgs = CHAT_DATABASE[target] || [];
    const container = document.getElementById("chatMessages");
    container.innerHTML = "";
    msgs.forEach(m => {
        const div = document.createElement("div");
        div.className = "chat-msg";
        div.innerHTML = `
            <div class="msg-avatar">${m.avatar}</div>
            <div class="msg-content">
                <div class="msg-header">
                    <span class="msg-author">${m.autor}</span>
                    <span class="msg-role">${m.role}</span>
                    <span class="msg-time">${m.hora}</span>
                </div>
                <div class="msg-text">${m.texto}</div>
            </div>
        `;
        container.appendChild(div);
    });
    container.scrollTop = container.scrollHeight;
}

function enviarMensagemChat() {
    const input = document.getElementById("chatInput");
    const val = input.value.trim();
    if (!val) return;
    input.value = "";
    sfxClick();

    const activeEl = document.querySelector(".chat-channel.active, .chat-dm.active");
    const target = activeEl ? (activeEl.dataset.channel || activeEl.dataset.npc) : "soc-geral";

    if (!CHAT_DATABASE[target]) CHAT_DATABASE[target] = [];
    CHAT_DATABASE[target].push({
        autor: "Matheus (Analista N1)",
        role: "Você",
        avatar: "🛡️",
        hora: formatTime(currentSeconds).substring(0, 5),
        texto: val
    });
    renderChatHistory(target);

    // Simulated NPC response after 2 seconds
    setTimeout(() => {
        const npcResponses = [
            "Excelente observação, Matheus. Vamos adicionar isso ao relatório.",
            "Copiado. Já estou analisando a telemetria aqui.",
            "Boa! Qualquer coisa me chama no ramal.",
            "Alerta devidamente registrado no log central."
        ];
        const randomResp = npcResponses[Math.floor(Math.random() * npcResponses.length)];
        CHAT_DATABASE[target].push({
            autor: "Ricardo (Senior)",
            role: "N3",
            avatar: "☕",
            hora: formatTime(currentSeconds).substring(0, 5),
            texto: randomResp
        });
        renderChatHistory(target);
    }, 2000);
}

// TERMINAL EVALUATOR
function execTerminal(cmd) {
    const termOutput = document.getElementById("termOutput");
    const res = processarComandoTerminal(cmd);
    if (res === "__CLEAR__") {
        termOutput.innerHTML = "";
        return;
    }
    termOutput.innerHTML += `\n<span style="color:#00ff88">matheus@soc-desk:~$</span> ${cmd}\n${res}\n`;
    termOutput.scrollTop = termOutput.scrollHeight;
}

// MOBILE TOUCH CONTROLS
function setupMobileControls() {
    const zone = document.getElementById("joystick-zone");
    const knob = document.getElementById("joystick-knob");
    let touchId = null;
    let startX = 0, startY = 0;

    zone.addEventListener("touchstart", (e) => {
        e.preventDefault();
        const t = e.changedTouches[0];
        touchId = t.identifier;
        const rect = zone.getBoundingClientRect();
        startX = rect.left + rect.width / 2;
        startY = rect.top + rect.height / 2;
    });

    zone.addEventListener("touchmove", (e) => {
        e.preventDefault();
        for (let i = 0; i < e.changedTouches.length; i++) {
            const t = e.changedTouches[i];
            if (t.identifier === touchId) {
                const dx = t.clientX - startX;
                const dy = t.clientY - startY;
                const dist = Math.min(40, Math.hypot(dx, dy));
                const angle = Math.atan2(dy, dx);
                knob.style.transform = `translate(${Math.cos(angle) * dist - 24}px, ${Math.sin(angle) * dist - 24}px)`;

                moveState.forward = dy < -10;
                moveState.backward = dy > 10;
                moveState.left = dx < -10;
                moveState.right = dx > 10;
            }
        }
    });

    const resetJoy = () => {
        touchId = null;
        knob.style.transform = "translate(-50%, -50%)";
        moveState.forward = false; moveState.backward = false;
        moveState.left = false; moveState.right = false;
    };
    zone.addEventListener("touchend", resetJoy);
    zone.addEventListener("touchcancel", resetJoy);

    document.getElementById("btnTouchInteract").addEventListener("click", () => {
        if (currentLookedObject && currentLookedObject.userData.interact) {
            currentLookedObject.userData.interact();
        }
    });
}

// TIME & SHIFT CLOCK
function formatTime(totalSec) {
    const h = String(Math.floor(totalSec / 3600)).padStart(2, '0');
    const m = String(Math.floor((totalSec % 3600) / 60)).padStart(2, '0');
    const s = String(totalSec % 60).padStart(2, '0');
    return `${h}:${m}:${s}`;
}

// ANIMATION LOOP
function animate() {
    requestAnimationFrame(animate);
    delta = clock.getDelta();

    // Update Shift Clock
    currentSeconds += delta * timeMultiplier;
    if (currentSeconds > 17 * 3600) currentSeconds = 17 * 3600;
    clockDisplay.innerText = `⏱️ ${formatTime(currentSeconds)}`;

    // Coffee drain over shift
    coffeeLevel = Math.max(0, coffeeLevel - delta * 0.05 * timeMultiplier);
    coffeeBar.style.width = `${coffeeLevel}%`;

    // Blinking Server LEDs
    serverLeds.forEach((led, i) => {
        if (Math.random() < 0.1) {
            led.visible = !led.visible;
        }
    });

    // Check Triggered Incidents
    INCIDENT_QUEUE.forEach(inc => {
        if (!inc.notificado && currentSeconds >= inc.horaSegundos) {
            inc.notificado = true;
            sfxSiren();
            if (inc.id === "INC-1042") {
                dispararChamadaTelefone("finance", "Juliana (Financeiro) no ramal: suspeita de Phishing!");
            }
        }
    });

    // Player Movement (WASD)
    if (!isSittingAtDesk) {
        velocity.x -= velocity.x * 10.0 * delta;
        velocity.z -= velocity.z * 10.0 * delta;

        direction.z = Number(moveState.forward) - Number(moveState.backward);
        direction.x = Number(moveState.right) - Number(moveState.left);
        direction.normalize();

        if (moveState.forward || moveState.backward) velocity.z -= direction.z * PLAYER_SPEED * 10.0 * delta;
        if (moveState.left || moveState.right) velocity.x -= direction.x * PLAYER_SPEED * 10.0 * delta;

        // Camera Forward Vector (Ignore Pitch)
        const forward = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), camera.rotation.y);
        const side = new THREE.Vector3(1, 0, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), camera.rotation.y);

        camera.position.addScaledVector(forward, -velocity.z * delta);
        camera.position.addScaledVector(side, velocity.x * delta);

        // Constrain in room boundaries
        camera.position.x = Math.max(-7.2, Math.min(7.2, camera.position.x));
        camera.position.z = Math.max(-7.2, Math.min(7.2, camera.position.z));
    }

    // Raycast Center of Screen for Interaction
    if (!isSittingAtDesk) {
        raycaster.setFromCamera(mouseCenter, camera);
        const intersects = raycaster.intersectObjects(interactableObjects, true);

        if (intersects.length > 0) {
            let hit = intersects[0].object;
            while (hit && !hit.userData.prompt && hit.parent) {
                hit = hit.parent;
            }

            if (hit && hit.userData && hit.userData.prompt) {
                currentLookedObject = hit;
                crosshairEl.classList.add("active");
                promptEl.innerText = hit.userData.prompt;
            } else {
                currentLookedObject = null;
                crosshairEl.classList.remove("active");
            }
        } else {
            currentLookedObject = null;
            crosshairEl.classList.remove("active");
        }
    }

    renderer.render(scene, camera);
}

// START ON LOAD
window.addEventListener("DOMContentLoaded", init);
