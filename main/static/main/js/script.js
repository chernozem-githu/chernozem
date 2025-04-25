document.addEventListener("visibilitychange", () => {
    const video = document.querySelector('.video-background video');
    if (document.visibilityState === 'visible' && video) {
        video.pause();
        video.currentTime = 0;
        video.play().catch(() => {});
    }
});
