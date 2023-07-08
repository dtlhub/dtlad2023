<script>
  import { onMount } from 'svelte';

  /** @type {number} */
  let w;
  /** @type {number} */
  let h;
  /** @type {string} */
  let color;
  /** @type {number} */
  let x;
  /** @type {number} */
  let y;
  /** @type {number} */
  const speedPixelsPerSecond = 20;
  /** @type {number} */
  let speedX;
  /** @type {number} */
  let speedY;
  /** @type {number} */
  let rotation;
  /** @type {number} */
  let rotationRadiansPerSecond = Math.PI * 0.25;
  /** @type {number} */
  let rotationSpeed;

  const colors = ['red', 'blue', 'yellow', 'lime', 'cyan', 'pink', 'white', 'purple'];

  /**
   * @param {any[]} array
   * @returns {any}
   */
  function chooseRandom(array) {
    return array[Math.floor(Math.random() * array.length)];
  }

  /**
   * @param {number} value
   * @param {number} min
   * @param {number} max
   * @returns {number}
   */
  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  onMount(() => {
    color = chooseRandom(colors);
    x = Math.random() * w;
    y = Math.random() * h;
    let direction = Math.random() * Math.PI * 2;
    speedX = Math.sin(direction) * (speedPixelsPerSecond / 60);
    speedY = Math.cos(direction) * (speedPixelsPerSecond / 60);
    rotation = Math.random() * Math.PI * 2;
    rotationSpeed = (rotationRadiansPerSecond / 60) * chooseRandom([-1, 1]);

    /**
     * @type {number}
     */
    let frame;

    function loop() {
      frame = requestAnimationFrame(loop);
      x += speedX;
      y += speedY;

      if (x < 0 || x > w) {
        speedX *= -1;
        x = clamp(x, 0, w);
      }
      if (y < 0 || y > h) {
        speedY *= -1;
        y = clamp(y, 0, h);
      }

      rotation += rotationSpeed;
    }

    loop();

    return () => cancelAnimationFrame(frame);
  });
</script>

<svelte:window bind:innerHeight={h} bind:innerWidth={w} />

<span
  style="
  color: var(--{color});
  top: {y}px;
  left: {x}px;
  transform: rotate({rotation}rad);
">ඞ</span
>

<style lang="scss">
  span {
    position: fixed;
    z-index: -1;
    user-select: none;
  }
</style>
