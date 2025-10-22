import {defineConfig} from 'vite';
import {resolve} from 'path';

/* Cesta ke statickému adresáři */
const djangoStaticRoot = resolve(__dirname, 'free_vat/static');

export default defineConfig({
    root: djangoStaticRoot,
    build: {
        /* Výstupní adresář */
        outDir: resolve(djangoStaticRoot, 'js/three/dist'),

        rollupOptions: {
            input: {
                main: resolve(djangoStaticRoot, 'js/three/src/main.js'),
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
    server: {
        origin: 'http://127.0.0.1:8000',
    }
});