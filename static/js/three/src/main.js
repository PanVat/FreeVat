import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader.js';
import {FBXLoader} from 'three/examples/jsm/loaders/FBXLoader.js';
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js';
// PŘIDÁNO: Import USDZLoaderu
import {USDZLoader} from 'three/examples/jsm/loaders/USDZLoader.js';

function init() {
    const container = document.getElementById('model-container');
    if (!container) return;

    const modelUrl = container.dataset.modelUrl;
    if (!modelUrl) {
        console.error("URL modelu nebyla nalezena.");
        return;
    }

    const extension = modelUrl.split('.').pop().toLowerCase();

    // --- Nastavení scény ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 2000);
    const renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});

    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;

    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // --- Posílené osvětlení ---
    scene.add(new THREE.AmbientLight(0xffffff, 1.2));
    const lights = [
        {pos: [10, 20, 10], int: 2.0},
        {pos: [-10, 10, -10], int: 1.5},
        {pos: [0, -10, 0], int: 0.8}
    ];
    lights.forEach(l => {
        const light = new THREE.DirectionalLight(0xffffff, l.int);
        light.position.set(...l.pos);
        scene.add(light);
    });

    // --- Ovládání ---
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    let initialCameraPos = new THREE.Vector3();
    let initialTarget = new THREE.Vector3();

    // --- Funkce pro zpracování modelu ---
    const setupModel = (object) => {
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        object.position.x += (object.position.x - center.x);
        object.position.y += (object.position.y - center.y);
        object.position.z += (object.position.z - center.z);

        const maxDim = Math.max(size.x, size.y, size.z);
        const distance = maxDim * 1.2;

        camera.position.set(distance, distance * 0.8, distance);
        camera.lookAt(0, 0, 0);
        controls.target.set(0, 0, 0);
        controls.update();

        initialCameraPos.copy(camera.position);
        initialTarget.copy(controls.target);

        let triangles = 0;
        let vertices = 0;
        object.traverse((child) => {
            if (child.isMesh) {
                const pos = child.geometry.attributes.position;
                if (pos) {
                    triangles += pos.count / 3;
                    vertices += pos.count;
                }
            }
        });

        const trisEl = document.getElementById('info-tris');
        const vertsEl = document.getElementById('info-verts');
        if (trisEl) trisEl.innerText = Math.round(triangles).toLocaleString();
        if (vertsEl) vertsEl.innerText = Math.round(vertices).toLocaleString();

        scene.add(object);
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'none';
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
            sceneContainer.requestFullscreen().catch(err => console.error(err));
        } else {
            document.exitFullscreen();
        }
    });

    // --- Loadery ---
    let loader;
    switch (extension) {
        case 'glb':
        case 'gltf':
            loader = new GLTFLoader();
            loader.load(modelUrl, (gltf) => setupModel(gltf.scene));
            break;
        case 'obj':
            loader = new OBJLoader();
            loader.load(modelUrl, (obj) => setupModel(obj));
            break;
        case 'fbx':
            loader = new FBXLoader();
            loader.load(modelUrl, (fbx) => setupModel(fbx));
            break;
        // PŘIDÁNO: Case pro USDZ
        case 'usdz':
            loader = new USDZLoader();
            loader.load(modelUrl, (usdz) => setupModel(usdz));
            break;
        case 'stl':
            loader = new STLLoader();
            loader.load(modelUrl, (geom) => {
                const mat = new THREE.MeshStandardMaterial({color: 0xcccccc, metalness: 0.2, roughness: 0.5});
                setupModel(new THREE.Mesh(geom, mat));
            });
            break;
        default:
            console.warn("Nepodporovaný formát souboru:", extension);
    }

    // --- Resize události ---
    const onResize = () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    };

    window.addEventListener('resize', onResize);
    document.addEventListener('fullscreenchange', onResize);

    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }

    animate();
}

init();