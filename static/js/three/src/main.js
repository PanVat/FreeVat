/* Importy základních modulů Three.js a loaderů pro různé 3D formáty */
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {OBJLoader} from 'three/examples/jsm/loaders/OBJLoader.js';
import {FBXLoader} from 'three/examples/jsm/loaders/FBXLoader.js';
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js';

/* Hlavní inicializační funkce prohlížeče */
function init() {
    /* Vyhledání kontejneru pro zobrazení modelu a získání URL modelu z data-atributu */
    const container = document.getElementById('model-container');
    if (!container) return;

    const modelUrl = container.dataset.modelUrl;
    if (!modelUrl) {
        console.error("URL modelu nebyla nalezena.");
        return;
    }

    /* Získání přípony souboru pro určení správného loaderu */
    const extension = modelUrl.split('.').pop().toLowerCase();
    console.log(`Načítám model: ${modelUrl} (přípona: ${extension})`);

    /* --- NASTAVENÍ SCÉNY A KAMERY --- */
    const scene = new THREE.Scene();

    /* Nastavení perspektivní kamery s širokým rozsahem vykreslování (clipping planes) */
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.01, 5000);

    /* Inicializace WebGL rendereru s vyhlazováním a průhledným pozadím */
    const renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});

    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    /* Nastavení mapování tónů a barevného prostoru pro realistický vzhled */
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    /* Vyčištění kontejneru a vložení plátna (canvas) prohlížeče */
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    /* Ambientní světlo pro základní prosvětlení stínů */
    scene.add(new THREE.AmbientLight(0xffffff, 1.5));

    /* Definice tří směrových světel pro vytvoření hloubky a nasvícení hran modelu */
    const lights = [
        {pos: [10, 20, 10], int: 2.5},   /* Hlavní světlo */
        {pos: [-10, 10, -10], int: 1.5}, /* Doplňkové světlo */
        {pos: [0, -10, 0], int: 1.0}     /* Spodní odrazové světlo */
    ];
    lights.forEach(l => {
        const light = new THREE.DirectionalLight(0xffffff, l.int);
        light.position.set(...l.pos);
        scene.add(light);
    });

    /* Umožňuje rotaci, zoom a posun kamery myší/dotykem */
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; /* Přidává setrvačnost při pohybu pro plynulost */
    controls.dampingFactor = 0.15;

    /* Proměnné pro uložení výchozího pohledu pro funkci Reset */
    let initialCameraPos = new THREE.Vector3();
    let initialTarget = new THREE.Vector3();

    /* --- FUNKCE PRO ZPRACOVÁNÍ A VYCENTROVÁNÍ MODELU --- */
    const setupModel = (object) => {
        if (!object) {
            console.error("Načtený objekt je prázdný.");
            return;
        }

        /* Výpočet bounding boxu (obálky) pro zjištění rozměrů a středu modelu */
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        console.log("Velikost modelu:", size);

        /* Přesun geometrie modelu do počátku souřadnic (0,0,0) */
        object.position.x -= center.x;
        object.position.y -= center.y;
        object.position.z -= center.z;

        /* Dynamický výpočet vzdálenosti kamery, aby byl model vidět celý bez ohledu na měřítko */
        const maxDim = Math.max(size.x, size.y, size.z);
        const distance = maxDim === 0 ? 5 : maxDim * 1.5;

        /* Nastavení pozice kamery a směru pohledu do středu */
        camera.position.set(distance, distance * 0.6, distance);
        camera.lookAt(0, 0, 0);

        controls.target.set(0, 0, 0);
        controls.update();

        /* Uložení aktuální pozice pro pozdější resetování pohledu */
        initialCameraPos.copy(camera.position);
        initialTarget.copy(controls.target);

        /* --- STATISTIKY MODELU (Triangles & Vertices) --- */
        let triangles = 0;
        let vertices = 0;
        /* Průchod všemi částmi modelu (meshe) a sčítání geometrických dat */
        object.traverse((child) => {
            if (child.isMesh) {
                const pos = child.geometry.attributes.position;
                if (pos) {
                    triangles += pos.count / 3;
                    vertices += pos.count;
                }
            }
        });

        /* Aktualizace informací v UI, formátování čísel podle lokálních zvyklostí */
        const trisEl = document.getElementById('info-tris');
        const vertsEl = document.getElementById('info-verts');
        if (trisEl) trisEl.innerText = Math.round(triangles).toLocaleString();
        if (vertsEl) vertsEl.innerText = Math.round(vertices).toLocaleString();

        /* Přidání finálně upraveného modelu do scény */
        scene.add(object);

        /* Odstranění načítací obrazovky po úspěšném nahrání */
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'none';

        console.log("Model úspěšně přidán do scény.");
    };

    /* Reset pohledu na výchozí pozici */
    document.getElementById('reset-view')?.addEventListener('click', () => {
        camera.position.copy(initialCameraPos);
        controls.target.copy(initialTarget);
        controls.update();
    });

    /* Přepínání celoobrazovkového režimu prohlížeče */
    document.getElementById('toggle-fullscreen')?.addEventListener('click', () => {
        const sceneContainer = document.querySelector('.model-3d-scene');
        if (!document.fullscreenElement) {
            sceneContainer.requestFullscreen().catch(err => console.error("Fullscreen error:", err));
        } else {
            document.exitFullscreen();
        }
    });

    /* Chybová funkce při selhání stahování souboru */
    const onError = (error) => {
        console.error("Chyba při načítání modelu:", error);
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.innerHTML = `<p style="color:red">Chyba při načítání modelu.</p>`;
    };

    /* Výběr správné třídy loaderu na základě přípony souboru */
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
            /* STL formát neobsahuje materiály, proto musíme vytvořit základní MeshStandardMaterial */
            new STLLoader().load(modelUrl, (geom) => {
                const mat = new THREE.MeshStandardMaterial({color: 0xcccccc, metalness: 0.2, roughness: 0.5});
                setupModel(new THREE.Mesh(geom, mat));
            }, undefined, onError);
            break;
        default:
            console.warn("Nepodporovaný formát souboru:", extension);
    }

    /* Zajišťuje, že prohlížeč správně reaguje na změnu velikosti okna prohlížeče */
    const onResize = () => {
        const width = container.clientWidth;
        const height = container.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    };

    window.addEventListener('resize', onResize);
    /* Speciální přepočet při vstupu/výstupu z fullscreenu s mírným zpožděním */
    document.addEventListener('fullscreenchange', () => {
        setTimeout(onResize, 100);
    });

    /* Renderovací smyčka běžící na frekvenci monitoru (60+ FPS) */
    function animate() {
        requestAnimationFrame(animate);
        controls.update(); /* Aktualizace setrvačnosti ovládání */
        renderer.render(scene, camera); /* Vykreslení aktuálního snímku */
    }

    animate();
}

/* Spuštění celého skriptu až po kompletním načtení struktury HTML stránky */
document.addEventListener('DOMContentLoaded', init);