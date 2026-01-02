import {defineConfig} from 'vite';
import {resolve} from 'path';

const djangoStaticRoot = resolve(__dirname, 'static');

export default defineConfig({
    /* Root je nastaven na static, takže cesty uvnitř budou relativní k němu */
    root: djangoStaticRoot,

    server: {
        /* Povolení přístupu z Django serveru */
        origin: 'http://localhost:8000',
        cors: true,
    },

    build: {
        /* Kam se uloží hotový soubor po 'npm run build' */
        outDir: resolve(djangoStaticRoot, 'js/three/dist'),
        emptyOutDir: true,
        rollupOptions: {
            input: {
                /* Zdrojový soubor, který se bude kompilovat */
                main: resolve(djangoStaticRoot, 'js/three/src/main.js'),
            },
            output: {
                entryFileNames: '[name].js', /* Vytvoří main.js */
                assetFileNames: 'assets/[name].[ext]',
            }
        },
    }
});