import {defineConfig} from 'vite';
import {resolve} from 'path';

/* Cesta ke statickému adresáři */
const djangoStaticRoot = resolve(__dirname, 'static');

export default defineConfig({
    root: djangoStaticRoot,
    build: {
        /* Výstupní adresář */
        outDir: resolve(djangoStaticRoot, 'js/three/dist'),

        rollupOptions: {
            input: {
                main: resolve(djangoStaticRoot, 'js/three/src/upload.js'),
            },
            output: {
                /* Názvy výstupního souboru */
                entryFileNames: '[name].js',
                assetFileNames: 'assets/[name].[ext]',
            }
        },
        emptyOutDir: true,
        manifest: true,
    },
    /* Konfigurace vývojového serveru */
    server: {
        origin: 'http://localhost:8000',
    }
});