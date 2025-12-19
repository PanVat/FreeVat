import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

function init() {
    const container = document.getElementById('model-container');

    if (!container) {
        console.error("Kontejner 'model-container' nebyl nalezen!");
        return;
    }

    // --- ZMĚNA: Testovací URL natvrdo ---
    // Používáme veřejný model robota, abychom otestovali funkčnost vieweru
    const modelUrl = 'https://threejs.org/examples/models/gltf/RobotExpressive/RobotExpressive.glb';

    console.log("Používám testovací model:", modelUrl);

    // --- Nastavení scény ---
    const scene = new THREE.Scene();

    // --- Kamera ---
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, 5, 15); // Trochu dál a výš

    // --- Renderer ---
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);

    // Vyčistíme kontejner (pro jistotu) a přidáme plátno
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // --- Světla ---
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
    directionalLight.position.set(5, 10, 7.5);
    scene.add(directionalLight);

    // --- Ovládání ---
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // --- Načítání modelu ---
    const loader = new GLTFLoader();

    loader.load(
        modelUrl,
        (gltf) => {
            const model = gltf.scene;
            scene.add(model);

            // Vycentrování modelu
            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());

            model.position.x += (model.position.x - center.x);
            model.position.y += (model.position.y - center.y);
            model.position.z += (model.position.z - center.z);

            // Skrytí overlaye (pokud existuje)
            const overlay = document.getElementById('loading-overlay');
            if (overlay) overlay.style.display = 'none';

            console.log("Testovací model úspěšně načten!");
        },
        (xhr) => {
            console.log((xhr.loaded / xhr.total * 100) + '% loaded');
        },
        (error) => {
            console.error('Chyba při načítání modelu:', error);
            alert("Chyba načítání: Podívej se do konzole (F12).");
        }
    );

    // --- Resize ---
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });

    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();
}

init();