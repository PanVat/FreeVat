import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

// ID kontejneru, který máte v index.html
const CONTAINER_ID = 'model-container';
const RENDER_HEIGHT = 500;

// Globální proměnné
let scene, camera, renderer, controls, clock;
let loadedModel; // Proměnná pro váš načtený model (nahradí 'cube')

// Cesta k vašemu 3D modelu. POZOR na to, že toto je URL, ne cesta na disku.
// Musí to odpovídat tomu, jak Django obsluhuje statické soubory.
const MODEL_PATH = '/static/models/scene.gltf'; // <-- Upravte na správnou cestu a název souboru!


function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function initializeScene() {
    const container = document.getElementById(CONTAINER_ID);

    if (!container) {
        console.error(`Kontejner s ID '${CONTAINER_ID}' nebyl nalezen!`);
        return;
    }

    const width = container.clientWidth;
    const height = RENDER_HEIGHT;

    // 1. Scéna a Kamera
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(
        45,
        width / height,
        1,
        1000
    );
    camera.position.set(0, 10, 30); // <-- Upravena pozice kamery, aby lépe viděla model

    // 2. Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    // 3. Doplňky
    clock = new THREE.Clock();
    controls = new OrbitControls(camera, renderer.domElement);

    // 4. Osvětlení (Ambientní a Směrové - kritické pro PBR materiály)
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    // 5. NAČTENÍ 3D MODELU (místo kostky)
    const loader = new GLTFLoader();
    loader.load(
        MODEL_PATH,
        (gltf) => {
            loadedModel = gltf.scene;
            scene.add(loadedModel);

            // Volitelné: Přizpůsobení měřítka, pozice, rotace modelu
            loadedModel.scale.set(10, 10, 10); // <-- Nastavte měřítko modelu, pokud je moc malý/velký
            loadedModel.position.set(0, 0, 0); // <-- Nastavte pozici modelu

            console.log('Model načten:', loadedModel);
        },
        (xhr) => {
            // Průběh načítání
            console.log((xhr.loaded / xhr.total * 100) + '% načteno');
        },
        (error) => {
            // Chyba načítání
            console.error('Při načítání modelu došlo k chybě:', error);
        }
    );
    // Konec načítání 3D modelu

    // 6. Reakce na Změnu Velikosti Okna
    window.addEventListener('resize', onWindowResize, false);

    // Spuštění animace
    animate();
}

// ... (onWindowResize, animate, render funkce zůstávají stejné, ale animate bude pracovat s loadedModel) ...

function animate() {
    window.requestAnimationFrame(animate);
    controls.update();
    render();
}

function render() {
    renderer.render(scene, camera);
}

// Spuštění celého inicializačního procesu
initializeScene();