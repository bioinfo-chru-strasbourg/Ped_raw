export const getBackendURL = () => {
    const url: string = import.meta.env.VITE_BACKEND;
    if (!url) {
        // For prod, path to server is defined in nginx config
        return "/api"
    } else {
        // For dev
        return url
    }
}