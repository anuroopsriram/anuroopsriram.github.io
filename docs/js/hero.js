/*
 * hero.js — "Crystal lattice field" WebGL2 hero animation.
 *
 * A sparse 3D crystal lattice of atoms (soft point sprites with fake
 * depth-of-field) connected by faint bonds, slowly rotating with a gentle
 * organic breathing displacement and a subtle cursor interaction (atoms near
 * the pointer are pushed aside and brightened, springing back on release).
 * Pure WebGL2 + GLSL, zero dependencies.
 *
 * ============================== INTEGRATION CONTRACT ==============================
 *
 * Expected DOM (home page hero):
 *
 *   <div class="hero">                        <!-- positioned container (any class) -->
 *     <canvas id="hero-canvas"></canvas>      <!-- absolutely positioned, fills container -->
 *     ... headline content ...
 *   </div>
 *   <script src=".../js/hero.js" defer></script>
 *
 * Initialization:
 *   - Auto-inits on DOMContentLoaded if a canvas with id "hero-canvas" exists.
 *   - Or call window.initHero(canvasSelectorOrElement[, options]) manually.
 *     `options` may override any key of DEFAULTS below (tuning knobs).
 *
 * Sizing:
 *   - The canvas is expected to be CSS-sized (e.g. position:absolute; inset:0;
 *     width:100%; height:100%). This script only manages the drawing-buffer
 *     resolution (devicePixelRatio capped at 2) via a ResizeObserver.
 *
 * Theming (CSS custom properties, read from <html> computed style):
 *   - --hero-atom-color   : atom sprite core color
 *   - --hero-bond-color   : bond line color
 *   - --hero-glow-color   : glow / pointer-highlight color
 *   Any valid CSS color (hex, rgb, oklch, ...) works. Fallbacks when unset:
 *     light theme: deep ink atoms (#22303a), teal bonds (#2f6f6a), copper glow (#b06a3f)
 *     dark theme:  warm white atoms (#efe9dd), teal bonds (#4fd8c4), teal glow (#7be8d8)
 *   Theme changes are detected live via a MutationObserver on the <html>
 *   `data-theme` attribute (set by theme.js). Blending adapts automatically:
 *   additive-ish glow on dark themes, normal alpha blending on light themes,
 *   branched on the luminance of the resolved atom color.
 *
 * Fallback:
 *   - If WebGL2 is unavailable OR prefers-reduced-motion matches (at load or at
 *     runtime), the animation does not run: the canvas is hidden and the class
 *     "hero-fallback" is added to the canvas's PARENT element. CSS should style
 *     `.hero-fallback` with a static gradient. No layout shift either way.
 *
 * Performance:
 *   - 60fps while the pointer is active, throttled to ~30fps after a few
 *     seconds idle, fully paused when the tab is hidden or the canvas is
 *     scrolled out of view (IntersectionObserver).
 * ==================================================================================
 */
(function () {
  'use strict';

  /* Tuning knobs (override via initHero(sel, {...})). */
  var DEFAULTS = {
    latticeSize: 7,          // lattice extends -N..N sites per axis (pre-culling)
    latticeSpacing: 0.7,     // distance between neighboring sites
    latticeRadius: 4.6,      // ellipsoid cull radius (world units)
    keepProbability: 0.8,    // chance a site inside the radius becomes an atom
    jitter: 0.18,            // random offset per site, fraction of spacing
    seed: 47,                // deterministic layout across reloads
    cameraDistance: 11.0,    // camera distance from lattice center
    fov: 33,                 // vertical field of view, degrees
    rotationSpeed: 0.035,    // radians/sec around Y (very slow)
    tiltAmount: 0.35,        // static tilt + slow wobble around X, radians
    breatheAmp: 0.075,       // organic displacement amplitude (world units)
    breatheSpeed: 0.5,       // organic displacement speed
    pointSize: 34.0,         // base sprite size in px at focus depth (pre-DPR)
    dofRange: 4.5,           // depth range over which sprites blur out
    atomAlpha: 0.9,          // peak atom opacity at focus depth
    bondAlpha: 0.16,         // peak bond opacity at focus depth
    pointerRadius: 2.4,      // interaction falloff radius (world units)
    pointerPush: 0.5,        // max displacement near pointer (world units)
    pointerStiffness: 5.0,   // spring stiffness of smoothed pointer follow
    idleDelay: 3000,         // ms without pointer movement before 30fps mode
    maxDpr: 2
  };

  var FALLBACK_CLASS = 'hero-fallback';

  var LIGHT_COLORS = { atom: '#22303a', bond: '#2f6f6a', glow: '#b06a3f' };
  var DARK_COLORS = { atom: '#efe9dd', bond: '#4fd8c4', glow: '#7be8d8' };

  /* ------------------------------------------------------------------ GLSL */

  // Shared vertex-shader chunk: breathing + rotation + pointer displacement.
  // Used verbatim by both programs so bonds track atoms exactly.
  var TRANSFORM_GLSL = [
    'uniform mat3 u_rot;',
    'uniform mat4 u_proj;',
    'uniform float u_time;',
    'uniform float u_camDist;',
    'uniform float u_breatheAmp;',
    'uniform float u_breatheSpeed;',
    'uniform vec3 u_pointer;',        // smoothed pointer, view space
    'uniform float u_pointerStrength;',
    'uniform float u_pointerRadius;',
    'uniform float u_pointerPush;',
    '',
    'vec3 breathe(vec3 p, vec3 seed) {',
    '  float a = u_time * u_breatheSpeed;',
    '  return u_breatheAmp * vec3(',
    '    sin(a         + seed.x * 6.2831 + p.y * 0.9),',
    '    sin(a * 1.13  + seed.y * 6.2831 + p.z * 0.9),',
    '    sin(a * 0.87  + seed.z * 6.2831 + p.x * 0.9));',
    '}',
    '',
    // Returns view-space position; writes pointer proximity (0..1) to `bright`.
    'vec3 latticeView(vec3 p, vec3 seed, out float bright) {',
    '  vec3 q = p + breathe(p, seed);',
    '  vec3 view = u_rot * q;',
    '  view.z -= u_camDist;',
    '  vec3 dp = view - u_pointer;',
    '  float fall = exp(-dot(dp, dp) / (u_pointerRadius * u_pointerRadius));',
    '  float s = fall * u_pointerStrength;',
    '  vec2 dir = dp.xy;',
    '  float len = max(length(dir), 1e-4);',
    '  view.xy += (dir / len) * s * u_pointerPush;',
    '  bright = s;',
    '  return view;',
    '}'
  ].join('\n');

  var ATOM_VS = [
    '#version 300 es',
    'in vec3 a_pos;',
    'in vec3 a_seed;',
    'uniform float u_pointSize;',
    'uniform float u_dofRange;',
    TRANSFORM_GLSL,
    'out float v_blur;',
    'out float v_bright;',
    'out float v_seed;',
    'void main() {',
    '  float bright;',
    '  vec3 view = latticeView(a_pos, a_seed, bright);',
    '  v_bright = bright;',
    '  v_seed = a_seed.x;',
    '  float depth = -view.z;',
    '  v_blur = clamp(abs(depth - u_camDist) / u_dofRange, 0.0, 1.0);',
    // Per-atom size variety; blurred (defocused) sprites swell like bokeh.
    '  float variety = 0.7 + 0.6 * a_seed.y;',
    '  float px = u_pointSize * variety * (1.0 + v_blur * 1.6) / depth;',
    '  gl_PointSize = clamp(px + bright * 6.0, 1.5, 96.0);',
    '  gl_Position = u_proj * vec4(view, 1.0);',
    '}'
  ].join('\n');

  var ATOM_FS = [
    '#version 300 es',
    'precision mediump float;',
    'uniform vec3 u_atomColor;',
    'uniform vec3 u_glowColor;',
    'uniform float u_atomAlpha;',
    'in float v_blur;',
    'in float v_bright;',
    'in float v_seed;',
    'out vec4 fragColor;',
    'void main() {',
    '  float d = length(gl_PointCoord - 0.5) * 2.0;',
    '  if (d > 1.0) discard;',
    // Defocused sprites get a softer, dimmer disc (fake depth of field).
    '  float edge = mix(0.35, 0.95, v_blur);',
    '  float disc = 1.0 - smoothstep(1.0 - edge, 1.0, d);',
    '  float core = 1.0 - smoothstep(0.0, 0.55, d);',
    '  float alpha = disc * u_atomAlpha * mix(1.0, 0.22, v_blur);',
    '  alpha *= 0.75 + 0.25 * v_seed;',
    '  alpha = min(alpha + v_bright * 0.35 * disc, 1.0);',
    '  vec3 color = mix(u_atomColor, u_glowColor, ',
    '                   clamp(v_bright * 0.9 + core * 0.15, 0.0, 1.0));',
    '  fragColor = vec4(color * alpha, alpha);',  // premultiplied
    '}'
  ].join('\n');

  var BOND_VS = [
    '#version 300 es',
    'in vec3 a_pos;',
    'in vec3 a_seed;',
    'uniform float u_dofRange;',
    TRANSFORM_GLSL,
    'out float v_fade;',
    'out float v_bright;',
    'void main() {',
    '  float bright;',
    '  vec3 view = latticeView(a_pos, a_seed, bright);',
    '  v_bright = bright;',
    '  float depth = -view.z;',
    '  float blur = clamp(abs(depth - u_camDist) / u_dofRange, 0.0, 1.0);',
    // Bonds fade with defocus and with distance from camera.
    '  v_fade = (1.0 - blur * 0.85) * clamp(2.2 - depth / u_camDist, 0.0, 1.0);',
    '  gl_Position = u_proj * vec4(view, 1.0);',
    '}'
  ].join('\n');

  var BOND_FS = [
    '#version 300 es',
    'precision mediump float;',
    'uniform vec3 u_bondColor;',
    'uniform vec3 u_glowColor;',
    'uniform float u_bondAlpha;',
    'in float v_fade;',
    'in float v_bright;',
    'out vec4 fragColor;',
    'void main() {',
    '  float alpha = u_bondAlpha * v_fade + v_bright * 0.12;',
    '  vec3 color = mix(u_bondColor, u_glowColor, clamp(v_bright, 0.0, 1.0));',
    '  fragColor = vec4(color * alpha, alpha);',  // premultiplied
    '}'
  ].join('\n');

  /* ------------------------------------------------------------- utilities */

  function mulberry32(seed) {
    var t = seed >>> 0;
    return function () {
      t = (t + 0x6d2b79f5) | 0;
      var r = Math.imul(t ^ (t >>> 15), 1 | t);
      r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
      return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Convert any CSS color string (hex, rgb, oklch, ...) to [r,g,b] in 0..1
  // via the canvas-2d fillStyle parser.
  var colorCtx = null;
  function cssColorToRgb(str, fallback) {
    if (!str || !str.trim()) str = fallback;
    if (!colorCtx) {
      var c = document.createElement('canvas');
      c.width = c.height = 1;
      colorCtx = c.getContext('2d', { willReadFrequently: true });
    }
    if (!colorCtx) return [0.5, 0.5, 0.5];
    colorCtx.clearRect(0, 0, 1, 1);
    colorCtx.fillStyle = fallback;
    colorCtx.fillStyle = str;   // invalid strings are ignored, keeping fallback
    colorCtx.fillRect(0, 0, 1, 1);
    var d = colorCtx.getImageData(0, 0, 1, 1).data;
    return [d[0] / 255, d[1] / 255, d[2] / 255];
  }

  function luminance(rgb) {
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
  }

  function compileProgram(gl, vsSrc, fsSrc) {
    function shader(type, src) {
      var s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
        var log = gl.getShaderInfoLog(s);
        gl.deleteShader(s);
        throw new Error('hero.js shader: ' + log);
      }
      return s;
    }
    var p = gl.createProgram();
    gl.attachShader(p, shader(gl.VERTEX_SHADER, vsSrc));
    gl.attachShader(p, shader(gl.FRAGMENT_SHADER, fsSrc));
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      throw new Error('hero.js link: ' + gl.getProgramInfoLog(p));
    }
    return p;
  }

  function perspective(fovDeg, aspect, near, far) {
    var f = 1 / Math.tan((fovDeg * Math.PI) / 360);
    var nf = 1 / (near - far);
    return new Float32Array([
      f / aspect, 0, 0, 0,
      0, f, 0, 0,
      0, 0, (far + near) * nf, -1,
      0, 0, 2 * far * near * nf, 0
    ]);
  }

  // Rotation: tilt around X, then spin around Y.
  function rotationMatrix(yaw, tilt) {
    var cy = Math.cos(yaw), sy = Math.sin(yaw);
    var cx = Math.cos(tilt), sx = Math.sin(tilt);
    // column-major mat3 = Rx * Ry
    return new Float32Array([
      cy, sx * sy, -cx * sy,
      0, cx, sx,
      sy, -sx * cy, cx * cy
    ]);
  }

  /* -------------------------------------------------------------- geometry */

  // Jittered cubic lattice culled to an ellipsoid; bonds join grid neighbors.
  function buildLattice(cfg) {
    var rand = mulberry32(cfg.seed);
    var n = cfg.latticeSize;
    var s = cfg.latticeSpacing;
    var positions = [];
    var seeds = [];
    var index = {};   // "i,j,k" -> atom index
    var count = 0;

    for (var i = -n; i <= n; i++) {
      for (var j = -n; j <= n; j++) {
        for (var k = -n; k <= n; k++) {
          var x = i * s, y = j * s, z = k * s;
          // Squash Y slightly so the field reads wide, like a hero band.
          var r = Math.sqrt(x * x + (y * 1.3) * (y * 1.3) + z * z);
          var edge = 1 - Math.min(r / cfg.latticeRadius, 1);
          // Sparser toward the edge for a soft silhouette.
          if (r > cfg.latticeRadius) continue;
          if (rand() > cfg.keepProbability * (0.35 + 0.65 * Math.sqrt(edge))) continue;
          var jx = (rand() * 2 - 1) * cfg.jitter * s;
          var jy = (rand() * 2 - 1) * cfg.jitter * s;
          var jz = (rand() * 2 - 1) * cfg.jitter * s;
          positions.push(x + jx, y + jy, z + jz);
          seeds.push(rand(), rand(), rand());
          index[i + ',' + j + ',' + k] = count++;
        }
      }
    }

    // Bond vertices duplicate atom pos+seed so shader displacement matches.
    var bondVerts = [];
    var bondSeeds = [];
    var dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    for (var key in index) {
      var abc = key.split(',');
      var a = index[key];
      for (var d = 0; d < 3; d++) {
        var nk = (+abc[0] + dirs[d][0]) + ',' + (+abc[1] + dirs[d][1]) + ',' +
                 (+abc[2] + dirs[d][2]);
        var b = index[nk];
        if (b === undefined) continue;
        bondVerts.push(
          positions[a * 3], positions[a * 3 + 1], positions[a * 3 + 2],
          positions[b * 3], positions[b * 3 + 1], positions[b * 3 + 2]);
        bondSeeds.push(
          seeds[a * 3], seeds[a * 3 + 1], seeds[a * 3 + 2],
          seeds[b * 3], seeds[b * 3 + 1], seeds[b * 3 + 2]);
      }
    }

    return {
      atomPos: new Float32Array(positions),
      atomSeed: new Float32Array(seeds),
      atomCount: count,
      bondPos: new Float32Array(bondVerts),
      bondSeed: new Float32Array(bondSeeds),
      bondVertexCount: bondVerts.length / 3
    };
  }

  /* ------------------------------------------------------------------ hero */

  function Hero(canvas, options) {
    var cfg = {};
    for (var k in DEFAULTS) cfg[k] = DEFAULTS[k];
    for (var o in (options || {})) cfg[o] = options[o];
    this.cfg = cfg;
    this.canvas = canvas;
    this.container = canvas.parentElement || document.body;
    this.reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    this.running = false;
    this.rafId = 0;
    this.visible = true;
    this.startTime = 0;
    this.lastFrame = 0;
    this.lastPointerMove = -Infinity;
    this.additiveBlend = false;
    // Smoothed pointer state (view space); strength eases in/out for
    // spring-back when the pointer leaves.
    this.pointerTarget = [0, 0, -cfg.cameraDistance];
    this.pointer = [0, 0, -cfg.cameraDistance];
    this.pointerStrength = 0;
    this.pointerActive = false;
  }

  Hero.prototype.fallback = function () {
    this.stop();
    this.canvas.style.display = 'none';
    this.container.classList.add(FALLBACK_CLASS);
  };

  Hero.prototype.init = function () {
    var self = this;

    if (this.reducedMotion.matches) { this.fallback(); return; }

    var gl = this.canvas.getContext('webgl2', {
      alpha: true,
      antialias: true,
      premultipliedAlpha: true,
      depth: false,
      powerPreference: 'low-power',
      // Keep the last frame available for re-composites outside the normal
      // rAF loop (printing, full-page captures); negligible cost here.
      preserveDrawingBuffer: true
    });
    if (!gl) { this.fallback(); return; }
    this.gl = gl;

    try {
      this.atomProgram = compileProgram(gl, ATOM_VS, ATOM_FS);
      this.bondProgram = compileProgram(gl, BOND_VS, BOND_FS);
    } catch (e) {
      this.fallback();
      return;
    }

    this.geometry = buildLattice(this.cfg);
    this.atomVao = this.makeVao(this.atomProgram, this.geometry.atomPos,
      this.geometry.atomSeed);
    this.bondVao = this.makeVao(this.bondProgram, this.geometry.bondPos,
      this.geometry.bondSeed);

    this.atomU = this.uniformMap(this.atomProgram);
    this.bondU = this.uniformMap(this.bondProgram);

    gl.disable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);

    this.readThemeColors();
    this.bindEvents();
    this.resize();
    this.start();
  };

  Hero.prototype.makeVao = function (program, posData, seedData) {
    var gl = this.gl;
    var vao = gl.createVertexArray();
    gl.bindVertexArray(vao);
    var posLoc = gl.getAttribLocation(program, 'a_pos');
    var seedLoc = gl.getAttribLocation(program, 'a_seed');
    var posBuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
    gl.bufferData(gl.ARRAY_BUFFER, posData, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(posLoc);
    gl.vertexAttribPointer(posLoc, 3, gl.FLOAT, false, 0, 0);
    var seedBuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, seedBuf);
    gl.bufferData(gl.ARRAY_BUFFER, seedData, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(seedLoc);
    gl.vertexAttribPointer(seedLoc, 3, gl.FLOAT, false, 0, 0);
    gl.bindVertexArray(null);
    return vao;
  };

  Hero.prototype.uniformMap = function (program) {
    var gl = this.gl;
    var map = {};
    var n = gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS);
    for (var i = 0; i < n; i++) {
      var info = gl.getActiveUniform(program, i);
      map[info.name] = gl.getUniformLocation(program, info.name);
    }
    return map;
  };

  Hero.prototype.readThemeColors = function () {
    var style = getComputedStyle(document.documentElement);
    var theme = document.documentElement.getAttribute('data-theme');
    var isDark = theme === 'dark';
    var fb = isDark ? DARK_COLORS : LIGHT_COLORS;
    this.atomColor = cssColorToRgb(
      style.getPropertyValue('--hero-atom-color'), fb.atom);
    this.bondColor = cssColorToRgb(
      style.getPropertyValue('--hero-bond-color'), fb.bond);
    this.glowColor = cssColorToRgb(
      style.getPropertyValue('--hero-glow-color'), fb.glow);
    // Luminous atoms on a dark page look best with additive-ish blending;
    // dark atoms on a light page need normal (premultiplied) alpha blending.
    this.additiveBlend = luminance(this.atomColor) > 0.5;
  };

  Hero.prototype.resize = function () {
    var dpr = Math.min(window.devicePixelRatio || 1, this.cfg.maxDpr);
    var w = Math.max(1, Math.round(this.canvas.clientWidth * dpr));
    var h = Math.max(1, Math.round(this.canvas.clientHeight * dpr));
    if (this.canvas.width !== w || this.canvas.height !== h) {
      this.canvas.width = w;
      this.canvas.height = h;
    }
    this.dpr = dpr;
    this.proj = perspective(this.cfg.fov, w / h, 0.1, 100);
    this.aspect = w / h;
    this.gl.viewport(0, 0, w, h);
  };

  // Unproject client coords onto the view-space plane through the lattice
  // center (z = -cameraDistance), where the pointer force lives.
  Hero.prototype.setPointerFromEvent = function (e) {
    var rect = this.canvas.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return;
    var nx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    var ny = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
    var tanHalf = Math.tan((this.cfg.fov * Math.PI) / 360);
    var d = this.cfg.cameraDistance;
    this.pointerTarget[0] = nx * tanHalf * this.aspect * d;
    this.pointerTarget[1] = ny * tanHalf * d;
    this.pointerTarget[2] = -d;
    this.pointerActive = true;
    this.lastPointerMove = performance.now();
    if (this.running && !this.rafId) this.scheduleFrame();
  };

  Hero.prototype.bindEvents = function () {
    var self = this;

    // If the GPU context is ever lost (driver reset, memory pressure), swap
    // to the CSS fallback instead of leaving a dead/blank canvas behind.
    this.onContextLost = function (e) {
      e.preventDefault();
      self.teardownToFallback();
    };
    this.canvas.addEventListener('webglcontextlost', this.onContextLost);

    this.onPointerMove = function (e) { self.setPointerFromEvent(e); };
    this.onPointerLeave = function () { self.pointerActive = false; };
    // Listen on the container so the interaction works through hero text.
    this.container.addEventListener('pointermove', this.onPointerMove);
    this.container.addEventListener('pointerleave', this.onPointerLeave);

    this.resizeObserver = new ResizeObserver(function () {
      self.resize();
    });
    this.resizeObserver.observe(this.canvas);

    this.intersectionObserver = new IntersectionObserver(function (entries) {
      self.visible = entries[entries.length - 1].isIntersecting;
      if (self.visible) self.start(); else self.stop();
    });
    this.intersectionObserver.observe(this.canvas);

    this.onVisibility = function () {
      if (document.hidden) self.stop();
      else if (self.visible) self.start();
    };
    document.addEventListener('visibilitychange', this.onVisibility);

    this.themeObserver = new MutationObserver(function () {
      self.readThemeColors();
      if (self.running && !self.rafId) self.scheduleFrame();
    });
    this.themeObserver.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme']
    });

    this.onReducedMotion = function (e) {
      if (e.matches) self.teardownToFallback();
    };
    if (this.reducedMotion.addEventListener) {
      this.reducedMotion.addEventListener('change', this.onReducedMotion);
    }
  };

  Hero.prototype.teardownToFallback = function () {
    if (this.resizeObserver) this.resizeObserver.disconnect();
    if (this.intersectionObserver) this.intersectionObserver.disconnect();
    if (this.themeObserver) this.themeObserver.disconnect();
    document.removeEventListener('visibilitychange', this.onVisibility);
    this.container.removeEventListener('pointermove', this.onPointerMove);
    this.container.removeEventListener('pointerleave', this.onPointerLeave);
    this.fallback();
  };

  Hero.prototype.start = function () {
    if (this.running || document.hidden || !this.visible) return;
    this.running = true;
    if (!this.startTime) this.startTime = performance.now();
    this.scheduleFrame();
  };

  Hero.prototype.stop = function () {
    this.running = false;
    if (this.rafId) {
      cancelAnimationFrame(this.rafId);
      this.rafId = 0;
    }
  };

  Hero.prototype.scheduleFrame = function () {
    var self = this;
    this.rafId = requestAnimationFrame(function (t) {
      self.rafId = 0;
      self.frame(t);
    });
  };

  Hero.prototype.frame = function (now) {
    if (!this.running) return;

    // ~30fps when the pointer has been idle for a while, 60fps otherwise.
    var idle = now - this.lastPointerMove > this.cfg.idleDelay;
    if (idle && now - this.lastFrame < 1000 / 32) {
      this.scheduleFrame();
      return;
    }
    var dt = Math.min((now - (this.lastFrame || now)) / 1000, 0.1);
    this.lastFrame = now;

    // Ease the smoothed pointer toward its target and its strength toward
    // 1 (active) or 0 (spring-back after leave/idle).
    var kp = 1 - Math.exp(-this.cfg.pointerStiffness * dt);
    this.pointer[0] += (this.pointerTarget[0] - this.pointer[0]) * kp;
    this.pointer[1] += (this.pointerTarget[1] - this.pointer[1]) * kp;
    this.pointer[2] += (this.pointerTarget[2] - this.pointer[2]) * kp;
    var targetStrength = (this.pointerActive && !idle) ? 1 : 0;
    var ks = 1 - Math.exp(-(targetStrength ? 4.0 : 2.0) * dt);
    this.pointerStrength += (targetStrength - this.pointerStrength) * ks;

    this.render((now - this.startTime) / 1000);
    this.scheduleFrame();
  };

  Hero.prototype.setSharedUniforms = function (u, time, rot) {
    var gl = this.gl;
    var cfg = this.cfg;
    gl.uniformMatrix3fv(u.u_rot, false, rot);
    gl.uniformMatrix4fv(u.u_proj, false, this.proj);
    gl.uniform1f(u.u_time, time);
    gl.uniform1f(u.u_camDist, cfg.cameraDistance);
    gl.uniform1f(u.u_breatheAmp, cfg.breatheAmp);
    gl.uniform1f(u.u_breatheSpeed, cfg.breatheSpeed);
    gl.uniform3fv(u.u_pointer, this.pointer);
    gl.uniform1f(u.u_pointerStrength, this.pointerStrength);
    gl.uniform1f(u.u_pointerRadius, cfg.pointerRadius);
    gl.uniform1f(u.u_pointerPush, cfg.pointerPush);
    gl.uniform1f(u.u_dofRange, cfg.dofRange);
    gl.uniform3fv(u.u_glowColor, this.glowColor);
  };

  Hero.prototype.render = function (time) {
    var gl = this.gl;
    var cfg = this.cfg;

    var yaw = time * cfg.rotationSpeed;
    var tilt = cfg.tiltAmount + Math.sin(time * 0.07) * 0.06;
    var rot = rotationMatrix(yaw, tilt);

    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    // Shaders output premultiplied alpha. On dark themes we let color
    // accumulate additively (glow); alpha still composites normally.
    if (this.additiveBlend) {
      gl.blendFuncSeparate(gl.ONE, gl.ONE, gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    } else {
      gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    }

    // Bonds first (behind), atoms on top.
    gl.useProgram(this.bondProgram);
    this.setSharedUniforms(this.bondU, time, rot);
    gl.uniform3fv(this.bondU.u_bondColor, this.bondColor);
    gl.uniform1f(this.bondU.u_bondAlpha, cfg.bondAlpha);
    gl.bindVertexArray(this.bondVao);
    gl.drawArrays(gl.LINES, 0, this.geometry.bondVertexCount);

    gl.useProgram(this.atomProgram);
    this.setSharedUniforms(this.atomU, time, rot);
    gl.uniform3fv(this.atomU.u_atomColor, this.atomColor);
    gl.uniform1f(this.atomU.u_atomAlpha, cfg.atomAlpha);
    gl.uniform1f(this.atomU.u_pointSize, cfg.pointSize * this.dpr);
    gl.bindVertexArray(this.atomVao);
    gl.drawArrays(gl.POINTS, 0, this.geometry.atomCount);

    gl.bindVertexArray(null);
  };

  /* ------------------------------------------------------------ public API */

  function initHero(canvasOrSelector, options) {
    var canvas = typeof canvasOrSelector === 'string'
      ? document.querySelector(canvasOrSelector)
      : canvasOrSelector;
    if (!canvas || !(canvas instanceof HTMLCanvasElement)) return null;
    var hero = new Hero(canvas, options);
    hero.init();
    return hero;
  }

  window.initHero = initHero;

  document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('hero-canvas');
    if (canvas && !canvas.dataset.heroInitialized) {
      canvas.dataset.heroInitialized = 'true';
      initHero(canvas);
    }
  });
})();
