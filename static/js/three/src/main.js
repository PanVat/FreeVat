import * as THREE from 'three';

import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';

import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {FBXLoader} from 'three/examples/jsm/loaders/FBXLoader.js';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader.js';
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js';

// ====== SCÉNA ======
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111827); // dark background

// ====== KAMERA ======
const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
camera.position.set(0, 2, 5);

// ====== RENDERER ======
const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: false
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;

document.getElementById('viewer').appendChild(renderer.domElement);

// ====== CONTROLS ======
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// ====== SVĚTLA ======
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
dirLight.position.set(5, 10, 7);
dirLight.castShadow = true;
scene.add(dirLight);

// ====== GRID (volitelné) ======
const grid = new THREE.GridHelper(10, 10, 0x444444, 0x222222);
scene.add(grid);

// ====== LOADERY ======
const gltfLoader = new GLTFLoader();
const fbxLoader = new FBXLoader();
const objLoader = new OBJLoader();
const stlLoader = new STLLoader();

let currentModel = null;

// ====== UNIVERZÁLNÍ LOADER ======
function loadModel(url) {
    clearScene();

    const ext = url.split('.').pop().toLowerCase();

    switch (ext) {
        case 'glb':
        case 'gltf':
            gltfLoader.load(url, (gltf) => {
                currentModel = gltf.scene;
                scene.add(currentModel);
                frameObject(currentModel);
            });
            break;

        case 'fbx':
            fbxLoader.load(url, (object) => {
                object.scale.set(0.01, 0.01, 0.01);
                currentModel = object;
                scene.add(currentModel);
                frameObject(currentModel);
            });
            break;

        case 'obj':
            objLoader.load(url, (object) => {
                currentModel = object;
                scene.add(currentModel);
                frameObject(currentModel);
            });
            break;

        case 'stl':
            stlLoader.load(url, (geometry) => {
                const material = new THREE.MeshStandardMaterial({
                    color: 0xcccccc,
                    metalness: 0.1,
                    roughness: 0.6
                });
                const mesh = new THREE.Mesh(geometry, material);
                currentModel = mesh;
                scene.add(currentModel);
                frameObject(currentModel);
            });
            break;

        default:
            console.error('Nepodporovaný formát:', ext);
    }
}

// ====== CENTROVÁNÍ + KAMERA ======
function frameObject(object) {
    const box = new THREE.Box3().setFromObject(object);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());

    object.position.sub(center);

    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / Math.tan(fov / 2));
    cameraZ *= 1.5;

    camera.position.set(0, maxDim * 0.5, cameraZ);
    camera.near = cameraZ / 100;
    camera.far = cameraZ * 100;
    camera.updateProjectionMatrix();

    controls.target.set(0, 0, 0);
    controls.update();
}

// ====== VYČIŠTĚNÍ SCÉNY ======
function clearScene() {
    if (!currentModel) return;

    scene.remove(currentModel);

    currentModel.traverse((child) => {
        if (child.geometry) child.geometry.dispose();
        if (child.material) {
            if (Array.isArray(child.material)) {
                child.material.forEach(mat => mat.dispose());
            } else {
                child.material.dispose();
            }
        }
    });

    currentModel = null;
}

// ====== RESIZE ======
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// ====== RENDER LOOP ======
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

animate();

// ====== EXPORT FUNKCE ======
// Zavoláš z Django šablony nebo JS:
// loadModel('/media/models/example.glb');

window.loadModel = loadModel;
