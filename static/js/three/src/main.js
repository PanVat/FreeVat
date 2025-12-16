import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';

// ID kontejneru v HTML
const CONTAINER_ID = 'model-container';

// Globální proměnné
let scene, camera, renderer, controls, loadedModel;

function onWindowResize() {
    const container = document.getElementById(CONTAINER_ID);
    if (!container || !camera || !renderer) return;

    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

function initializeScene() {
    const container = document.getElementById(CONTAINER_ID);

    if (!container) {
        console.warn(`Kontejner s ID '${CONTAINER_ID}' nebyl na této stránce nalezen.`);
        return;
    }

    // --- ZÍSKÁNÍ CESTY K MODELU Z HTML ---
    // Toto je klíčová změna. Čteme atribut data-model-url.
    const modelUrl = container.getAttribute('data-model-url');

    if (!modelUrl) {
        console.error('Atribut data-model-url je prázdný!');
        return;
    }

    // Získání rozměrů přímo z rodičovského divu (aby byl responzivní)
    const width = container.clientWidth;
    const height = container.clientHeight;

    // 1. Scéna a Kamera
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf3f4f6); // Světle šedé pozadí (Tailwind gray-100)

    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 5, 10);

    // 2. Renderer
    renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio); // Pro ostrý obraz na mobilech

    // Přidání rendereru do stránky
    container.innerHTML = ''; // Vyčištění pro jistotu
    container.appendChild(renderer.domElement);

    // 3. Ovládání (OrbitControls)
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Plynulý dojezd
    controls.dampingFactor = 0.05;

    // 4. Osvětlení
    const ambientLight = new THREE.AmbientLight(0xffffff, 1);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
    directionalLight.position.set(5, 10, 7);
    scene.add(directionalLight);

    // 5. Načtení modelu
    const loader = new GLTFLoader();

    // Zobrazení loading textu (pokud ho v HTML máte)
    const loadingOverlay = document.getElementById('loading-overlay');

    loader.load(
        modelUrl, // Zde používáme dynamickou URL z Django
        (gltf) => {
            loadedModel = gltf.scene;
            scene.add(loadedModel);

            // Automatické vycentrování modelu
            const box = new THREE.Box3().setFromObject(loadedModel);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());

            // Reset pozice modelu na střed
            loadedModel.position.x += (loadedModel.position.x - center.x);
            loadedModel.position.y += (loadedModel.position.y - center.y);
            loadedModel.position.z += (loadedModel.position.z - center.z);

            // Automatický zoom kamery podle velikosti objektu
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / 2 * Math.tan(fov * 2));
            cameraZ *= 2.5; // Zoom out faktor
            camera.position.z = cameraZ;

            controls.target.set(0, 0, 0);

            // Skrytí loading overlay
            if (loadingOverlay) loadingOverlay.style.display = 'none';

            console.log('Model úspěšně načten z:', modelUrl);
        },
        (xhr) => {
            // Progress
            if (xhr.total > 0) {
                const percent = (xhr.loaded / xhr.total * 100).toFixed(0);
                if (loadingOverlay) loadingOverlay.innerText = `Načítám... ${percent}%`;
            }
        },
        (error) => {
            console.error('Chyba při načítání modelu:', error);
            if (loadingOverlay) loadingOverlay.innerText = 'Chyba při načítání modelu.';
        }
    );

    // 6. Resize listener
    window.addEventListener('resize', onWindowResize, false);

    // Spuštění smyčky
    animate();
}

function animate() {
    requestAnimationFrame(animate);
    if (controls) controls.update();
    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}

// Spuštění po načtení DOMu
document.addEventListener('DOMContentLoaded', initializeScene);