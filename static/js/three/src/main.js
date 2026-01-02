import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';

function init() {
    const container = document.getElementById('model-container');
    if (!container) return;

    const modelUrl = container.dataset.modelUrl;
    if (!modelUrl) {
        console.error("URL modelu nebyla nalezena.");
        return;
    }

    const extension = modelUrl.split('.').pop().toLowerCase();
    console.log(`Načítám model: ${modelUrl} (přípona: ${extension})`);

    // --- Nastavení scény ---
    const scene = new THREE.Scene();

    // Rozšířené clipping planes (0.01 až 5000), aby modely nemizely při přiblížení/oddálení
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.01, 5000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.outputColorSpace = THREE.SRGBColorSpace; // Zajišťuje správné barvy

    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // --- Osvětlení ---
    scene.add(new THREE.AmbientLight(0xffffff, 1.5));
    const lights = [
        { pos: [10, 20, 10], int: 2.5 },
        { pos: [-10, 10, -10], int: 1.5 },
        { pos: [0, -10, 0], int: 1.0 }
    ];
    lights.forEach(l => {
        const light = new THREE.DirectionalLight(0xffffff, l.int);
        light.position.set(...l.pos);
        scene.add(light);
    });

    // --- Ovládání ---
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.15;

    let initialCameraPos = new THREE.Vector3();
    let initialTarget = new THREE.Vector3();

    // --- Funkce pro zpracování modelu ---
    const setupModel = (object) => {
        if (!object) {
            console.error("Načtený objekt je prázdný.");
            return;
        }

        // Výpočet bounding boxu pro správné vycentrování a zoom
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        console.log("Velikost modelu:", size);

        // Vycentrování geometrie modelu (posuneme objekt o středový vektor zpět)
        object.position.x -= center.x;
        object.position.y -= center.y;
        object.position.z -= center.z;

        // Výpočet vzdálenosti kamery na základě velikosti modelu
        const maxDim = Math.max(size.x, size.y, size.z);

        // Pojistka pro extrémně malé modely (pokud je maxDim 0, dáme default 5)
        const distance = maxDim === 0 ? 5 : maxDim * 1.5;

        camera.position.set(distance, distance * 0.6, distance);
        camera.lookAt(0, 0, 0);

        controls.target.set(0, 0, 0);
        controls.update();

        // Uložení stavu pro Reset
        initialCameraPos.copy(camera.position);
        initialTarget.copy(controls.target);

        // Statistiky
        let triangles = 0;
        let vertices = 0;
        object.traverse((child) => {
            if (child.isMesh) {
                const pos = child.geometry.attributes.position;
                if (pos) {
                    // Počet bodů / 3 = počet trojúhelníků
                    triangles += pos.count / 3;
                    vertices += pos.count;
                }
            }
        });

        // Update UI prvků (Triangles/Vertices)
        const trisEl = document.getElementById('info-tris');
        const vertsEl = document.getElementById('info-verts');
        if (trisEl) trisEl.innerText = Math.round(triangles).toLocaleString();
        if (vertsEl) vertsEl.innerText = Math.round(vertices).toLocaleString();

        scene.add(object);

        // Skrytí loading overlay
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'none';

        console.log("Model úspěšně přidán do scény.");
    };

    // --- Logika tlačítek ---
    document.getElementById('reset-view')?.addEventListener('click', () => {
        camera.position.copy(initialCameraPos);
        controls.target.copy(initialTarget);
        controls.update();
    });

    document.getElementById('toggle-fullscreen')?.addEventListener('click', () => {
        const sceneContainer = document.querySelector('.model-3d-scene');
        if (!document.fullscreenElement) {
            sceneContainer.requestFullscreen().catch(err => console.error("Fullscreen error:", err));
        } else {
            document.exitFullscreen();
        }
    });

    // --- Loadery ---
    const onError = (error) => {
        console.error("Chyba při načítání modelu:", error);
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.innerHTML = `<p style="color:red">Chyba při načítání modelu.</p>`;
    };

    switch (extension) {
        case 'glb':
        case 'gltf':
            new GLTFLoader().load(modelUrl, (gltf) => setupModel(gltf.scene), undefined, onError);
            break;
        case 'obj':
            new OBJLoader().load(modelUrl, (obj) => setupModel(obj), undefined, onError);
            break;
        case 'fbx':
            new FBXLoader().load(modelUrl, (fbx) => setupModel(fbx), undefined, onError);
            break;
        case 'stl':
            new STLLoader().load(modelUrl, (geom) => {
                const mat = new THREE.MeshStandardMaterial({ color: 0xcccccc, metalness: 0.2, roughness: 0.5 });
                setupModel(new THREE.Mesh(geom, mat));
            }, undefined, onError);
            break;
        default:
            console.warn("Nepodporovaný formát souboru:", extension);
    }

    // --- Resize a Animate ---
    const onResize = () => {
        const width = container.clientWidth;
        const height = container.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    };

    window.addEventListener('resize', onResize);
    document.addEventListener('fullscreenchange', () => {
        setTimeout(onResize, 100); // Malé zpoždění pro správný výpočet v fullscreenu
    });

    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }

    animate();
}

// Spustit až po načtení DOMu
document.addEventListener('DOMContentLoaded', init);