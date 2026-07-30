/*
 * Research Field
 * A progressive WebGPU particle field with WebGL2 and static CSS fallbacks.
 * Essential content remains ordinary DOM above this decorative canvas.
 */

const canvas = document.querySelector('[data-research-field] #hero-canvas');
const hero = canvas?.closest('[data-research-field]');

if (canvas && hero) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const saveData = navigator.connection?.saveData === true;

  if (reducedMotion.matches || saveData) {
    setStaticFallback(saveData ? 'save-data' : 'reduced-motion');
  } else {
    init().catch(() => loadWebGLFallback());
  }
}

async function init() {
  if (!navigator.gpu || navigator.userAgent.includes('HeadlessChrome')) {
    await loadWebGLFallback();
    return;
  }

  const adapter = await navigator.gpu.requestAdapter({
    powerPreference: matchMedia('(max-width: 720px)').matches
      ? 'low-power'
      : 'high-performance',
  });
  if (!adapter) {
    await loadWebGLFallback();
    return;
  }

  const device = await adapter.requestDevice();
  const context = canvas.getContext('webgpu');
  if (!context) {
    await loadWebGLFallback();
    return;
  }

  const renderer = new ResearchField(device, context);
  await renderer.init();
  hero.dataset.renderer = 'webgpu';

  device.lost.then(() => {
    renderer.destroy();
    loadWebGLFallback();
  });
}

class ResearchField {
  constructor(device, context) {
    this.device = device;
    this.context = context;
    this.count = matchMedia('(max-width: 720px)').matches ? 260 : 520;
    this.format = navigator.gpu.getPreferredCanvasFormat();
    this.visible = true;
    this.running = false;
    this.pointer = { x: 0, y: 0, strength: 0, active: false };
    this.chapter = 2;
    this.lastFrame = 0;
    this.startTime = performance.now();
    this.frameHandle = 0;
    this.destroyed = false;
  }

  async init() {
    this.context.configure({
      device: this.device,
      format: this.format,
      alphaMode: 'premultiplied',
    });

    this.createParticles();
    this.createPipelines();
    this.createBindings();
    this.bindEvents();
    this.resize();
    this.start();
  }

  createParticles() {
    const floatsPerParticle = 6;
    const data = new Float32Array(this.count * floatsPerParticle);
    const random = mulberry32(47);

    for (let i = 0; i < this.count; i += 1) {
      const offset = i * floatsPerParticle;
      const radius = Math.sqrt(random()) * 0.9;
      const angle = random() * Math.PI * 2;
      data[offset] = Math.cos(angle) * radius;
      data[offset + 1] = Math.sin(angle) * radius;
      data[offset + 2] = 0;
      data[offset + 3] = 0;
      data[offset + 4] = random();
      data[offset + 5] = i % 4;
    }

    this.particleBuffer = this.device.createBuffer({
      label: 'research-field-particles',
      size: data.byteLength,
      usage:
        GPUBufferUsage.STORAGE |
        GPUBufferUsage.COPY_DST |
        GPUBufferUsage.VERTEX,
    });
    this.device.queue.writeBuffer(this.particleBuffer, 0, data);

    this.uniformData = new Float32Array(8);
    this.uniformBuffer = this.device.createBuffer({
      label: 'research-field-uniforms',
      size: this.uniformData.byteLength,
      usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
    });

    const quad = new Float32Array([
      -1, -1, 1, -1, -1, 1,
      -1, 1, 1, -1, 1, 1,
    ]);
    this.quadBuffer = this.device.createBuffer({
      label: 'research-field-quad',
      size: quad.byteLength,
      usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
    });
    this.device.queue.writeBuffer(this.quadBuffer, 0, quad);
  }

  createPipelines() {
    const computeModule = this.device.createShaderModule({
      label: 'research-field-compute-shader',
      code: COMPUTE_SHADER,
    });
    const renderModule = this.device.createShaderModule({
      label: 'research-field-render-shader',
      code: RENDER_SHADER,
    });

    this.computePipeline = this.device.createComputePipeline({
      label: 'research-field-compute',
      layout: 'auto',
      compute: { module: computeModule, entryPoint: 'main' },
    });

    this.renderPipeline = this.device.createRenderPipeline({
      label: 'research-field-render',
      layout: 'auto',
      vertex: {
        module: renderModule,
        entryPoint: 'vertexMain',
        buffers: [
          {
            arrayStride: 8,
            attributes: [{ shaderLocation: 0, offset: 0, format: 'float32x2' }],
          },
        ],
      },
      fragment: {
        module: renderModule,
        entryPoint: 'fragmentMain',
        targets: [
          {
            format: this.format,
            blend: {
              color: {
                srcFactor: 'src-alpha',
                dstFactor: 'one',
                operation: 'add',
              },
              alpha: {
                srcFactor: 'one',
                dstFactor: 'one-minus-src-alpha',
                operation: 'add',
              },
            },
          },
        ],
      },
      primitive: { topology: 'triangle-list' },
    });
  }

  createBindings() {
    const entries = [
      { binding: 0, resource: { buffer: this.particleBuffer } },
      { binding: 1, resource: { buffer: this.uniformBuffer } },
    ];
    this.computeBindGroup = this.device.createBindGroup({
      layout: this.computePipeline.getBindGroupLayout(0),
      entries,
    });
    this.renderBindGroup = this.device.createBindGroup({
      layout: this.renderPipeline.getBindGroupLayout(0),
      entries,
    });
  }

  bindEvents() {
    this.onPointerMove = (event) => {
      const rect = canvas.getBoundingClientRect();
      this.pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      this.pointer.y = -(((event.clientY - rect.top) / rect.height) * 2 - 1);
      this.pointer.active = true;
      this.start();
    };
    this.onPointerLeave = () => {
      this.pointer.active = false;
    };
    hero.addEventListener('pointermove', this.onPointerMove, { passive: true });
    hero.addEventListener('pointerleave', this.onPointerLeave);

    this.resizeObserver = new ResizeObserver(() => this.resize());
    this.resizeObserver.observe(canvas);

    this.visibilityObserver = new IntersectionObserver((entries) => {
      this.visible = entries.at(-1)?.isIntersecting ?? false;
      if (this.visible) this.start();
      else this.stop();
    });
    this.visibilityObserver.observe(canvas);

    this.chapterObserver = new IntersectionObserver(
      (entries) => {
        const active = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (active) {
          this.chapter = Number(active.target.dataset.fieldChapter || 0);
        }
      },
      { rootMargin: '-25% 0px -35%', threshold: [0.1, 0.35, 0.65] },
    );
    document
      .querySelectorAll('[data-field-chapter]')
      .forEach((chapter) => this.chapterObserver.observe(chapter));

    this.onVisibilityChange = () => {
      if (document.hidden) this.stop();
      else this.start();
    };
    document.addEventListener('visibilitychange', this.onVisibilityChange);

    this.onReducedMotion = (event) => {
      if (event.matches) {
        this.destroy();
        setStaticFallback('reduced-motion');
      }
    };
    reducedMotion.addEventListener('change', this.onReducedMotion);
  }

  resize() {
    const mobile = matchMedia('(max-width: 720px)').matches;
    const dpr = Math.min(devicePixelRatio || 1, mobile ? 1.25 : 1.75);
    const width = Math.max(1, Math.round(canvas.clientWidth * dpr));
    const height = Math.max(1, Math.round(canvas.clientHeight * dpr));
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
    }
    this.aspect = width / height;
  }

  start() {
    if (this.destroyed || this.running || !this.visible || document.hidden) return;
    this.running = true;
    this.frameHandle = requestAnimationFrame((time) => this.frame(time));
  }

  stop() {
    this.running = false;
    cancelAnimationFrame(this.frameHandle);
    this.frameHandle = 0;
  }

  frame(time) {
    if (!this.running || this.destroyed) return;

    const idle = !this.pointer.active && time - this.lastFrame < 1000 / 32;
    if (idle) {
      this.frameHandle = requestAnimationFrame((next) => this.frame(next));
      return;
    }

    const dt = Math.min((time - (this.lastFrame || time)) / 1000, 0.05);
    this.lastFrame = time;
    const targetStrength = this.pointer.active ? 1 : 0;
    this.pointer.strength +=
      (targetStrength - this.pointer.strength) * (1 - Math.exp(-dt * 4));

    this.uniformData.set([
      (time - this.startTime) / 1000,
      dt,
      this.pointer.x,
      this.pointer.y,
      this.pointer.strength,
      this.chapter,
      this.aspect,
      this.count,
    ]);
    this.device.queue.writeBuffer(this.uniformBuffer, 0, this.uniformData);
    this.render();

    this.frameHandle = requestAnimationFrame((next) => this.frame(next));
  }

  render() {
    const encoder = this.device.createCommandEncoder({
      label: 'research-field-frame',
    });
    const computePass = encoder.beginComputePass();
    computePass.setPipeline(this.computePipeline);
    computePass.setBindGroup(0, this.computeBindGroup);
    computePass.dispatchWorkgroups(Math.ceil(this.count / 64));
    computePass.end();

    const renderPass = encoder.beginRenderPass({
      colorAttachments: [
        {
          view: this.context.getCurrentTexture().createView(),
          clearValue: { r: 0, g: 0, b: 0, a: 0 },
          loadOp: 'clear',
          storeOp: 'store',
        },
      ],
    });
    renderPass.setPipeline(this.renderPipeline);
    renderPass.setBindGroup(0, this.renderBindGroup);
    renderPass.setVertexBuffer(0, this.quadBuffer);
    renderPass.draw(6, this.count);
    renderPass.end();

    this.device.queue.submit([encoder.finish()]);
  }

  destroy() {
    if (this.destroyed) return;
    this.destroyed = true;
    this.stop();
    this.resizeObserver?.disconnect();
    this.visibilityObserver?.disconnect();
    this.chapterObserver?.disconnect();
    hero.removeEventListener('pointermove', this.onPointerMove);
    hero.removeEventListener('pointerleave', this.onPointerLeave);
    document.removeEventListener('visibilitychange', this.onVisibilityChange);
    reducedMotion.removeEventListener('change', this.onReducedMotion);
    this.particleBuffer?.destroy();
    this.uniformBuffer?.destroy();
    this.quadBuffer?.destroy();
  }
}

async function loadWebGLFallback() {
  if (!canvas || !hero || hero.dataset.renderer === 'webgl2') return;
  hero.dataset.renderer = 'webgl2';
  canvas.dataset.heroInitialized = 'true';

  await new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = new URL('./hero.js', import.meta.url).href;
    script.onload = resolve;
    script.onerror = reject;
    document.head.append(script);
  });

  const instance = window.initHero?.(canvas, {
    latticeSize: 8,
    latticeRadius: 5.2,
    keepProbability: 0.72,
    rotationSpeed: 0.024,
    pointSize: 30,
    bondAlpha: 0.1,
    maxDpr: matchMedia('(max-width: 720px)').matches ? 1.25 : 1.75,
  });
  if (!instance) setStaticFallback('webgl-unavailable');
}

function setStaticFallback(reason) {
  if (!canvas || !hero) return;
  canvas.style.display = 'none';
  hero.classList.add('hero-fallback');
  hero.dataset.renderer = reason;
}

function mulberry32(seed) {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) | 0;
    let value = Math.imul(state ^ (state >>> 15), 1 | state);
    value = (value + Math.imul(value ^ (value >>> 7), 61 | value)) ^ value;
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

const COMPUTE_SHADER = /* wgsl */ `
struct Particle {
  position: vec2f,
  velocity: vec2f,
  seed: vec2f,
}

struct Uniforms {
  time: f32,
  delta: f32,
  pointerX: f32,
  pointerY: f32,
  pointerStrength: f32,
  chapter: f32,
  aspect: f32,
  count: f32,
}

@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;
@group(0) @binding(1) var<uniform> uniforms: Uniforms;

fn center(cluster: f32, chapter: f32) -> vec2f {
  let base = array<vec2f, 4>(
    vec2f(-0.52, 0.34),
    vec2f(0.42, 0.45),
    vec2f(-0.28, -0.36),
    vec2f(0.52, -0.28)
  );
  let focus = base[u32(chapter) % 4u];
  let own = base[u32(cluster) % 4u];
  return mix(own, focus * 0.42, 0.2);
}

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) id: vec3u) {
  let index = id.x;
  if (index >= u32(uniforms.count)) {
    return;
  }

  var particle = particles[index];
  let cluster = particle.seed.y;
  let origin = center(cluster, uniforms.chapter);
  let angle = particle.seed.x * 6.283185 + uniforms.time * (0.035 + cluster * 0.008);
  let band = 0.1 + fract(particle.seed.x * 17.0) * 0.34;
  let ellipse = vec2f(cos(angle) * band / max(uniforms.aspect, 0.7), sin(angle) * band);
  let wave = vec2f(
    sin(uniforms.time * 0.17 + particle.seed.x * 21.0),
    cos(uniforms.time * 0.13 + particle.seed.x * 15.0)
  ) * 0.025;
  let target = origin + ellipse + wave;

  let pointer = vec2f(uniforms.pointerX, uniforms.pointerY);
  let deltaPointer = particle.position - pointer;
  let pointerDistance = max(length(deltaPointer), 0.015);
  let pointerForce = normalize(deltaPointer) *
    exp(-pointerDistance * 4.5) * uniforms.pointerStrength * 0.42;

  let acceleration = (target - particle.position) * 1.25 + pointerForce;
  particle.velocity = (particle.velocity + acceleration * uniforms.delta) *
    exp(-uniforms.delta * 1.8);
  particle.position += particle.velocity * uniforms.delta;
  particles[index] = particle;
}
`;

const RENDER_SHADER = /* wgsl */ `
struct Particle {
  position: vec2f,
  velocity: vec2f,
  seed: vec2f,
}

struct Uniforms {
  time: f32,
  delta: f32,
  pointerX: f32,
  pointerY: f32,
  pointerStrength: f32,
  chapter: f32,
  aspect: f32,
  count: f32,
}

struct VertexOutput {
  @builtin(position) position: vec4f,
  @location(0) uv: vec2f,
  @location(1) seed: f32,
  @location(2) cluster: f32,
}

@group(0) @binding(0) var<storage, read> particles: array<Particle>;
@group(0) @binding(1) var<uniform> uniforms: Uniforms;

@vertex
fn vertexMain(
  @location(0) corner: vec2f,
  @builtin(instance_index) instance: u32
) -> VertexOutput {
  let particle = particles[instance];
  let speed = length(particle.velocity);
  let size = (0.0028 + particle.seed.x * 0.0045 + speed * 0.004);
  let offset = corner * vec2f(size / max(uniforms.aspect, 0.7), size);

  var output: VertexOutput;
  output.position = vec4f(particle.position + offset, 0.0, 1.0);
  output.uv = corner;
  output.seed = particle.seed.x;
  output.cluster = particle.seed.y;
  return output;
}

@fragment
fn fragmentMain(input: VertexOutput) -> @location(0) vec4f {
  let distanceFromCenter = length(input.uv);
  if (distanceFromCenter > 1.0) {
    discard;
  }

  let edge = 1.0 - smoothstep(0.15, 1.0, distanceFromCenter);
  let cyan = vec3f(0.30, 0.93, 0.84);
  let amber = vec3f(1.0, 0.70, 0.30);
  let paper = vec3f(0.96, 0.94, 0.87);
  let domain = select(cyan, amber, input.cluster == 3.0);
  let color = mix(paper, domain, 0.38 + input.seed * 0.42);
  let alpha = edge * (0.32 + input.seed * 0.58);
  return vec4f(color, alpha);
}
`;
