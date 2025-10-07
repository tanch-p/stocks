import { ref, onMounted, onUnmounted } from 'vue'

export function useViewport(maxWidth = 1024) {
  const isMobileOrTablet = ref(false)
  const media = window.matchMedia(`(max-width: ${maxWidth}px)`)

  function update(e) {
    isMobileOrTablet.value = e.matches
  }

  onMounted(() => {
    update(media)
    media.addEventListener('change', update)
  })

  onUnmounted(() => {
    media.removeEventListener('change', update)
  })

  return { isMobileOrTablet }
}
