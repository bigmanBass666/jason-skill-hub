# WebGL / Three.js 高级模式参考

> 面向 Awwwards 级别网站的前端 3D 开发模式手册。涵盖 Three.js、GLSL 着色器、粒子系统、性能优化、WebGPU 与 3D 资产管线。

---

## 目录

1. [Three.js 核心初始化](#1-threejs-核心初始化)
2. [粒子系统](#2-粒子系统)
3. [流体/有机形态](#3-流体有机形态)
4. [GLSL 着色器特效](#4-glsl-着色器特效)
5. [WebGL 性能优化](#5-webgl-性能优化)
6. [WebGPU（2026 下一代）](#6-webgpu2026-下一代)
7. [3D 资产管线](#7-3d-资产管线)
8. [鼠标/滚动交互](#8-鼠标滚动交互)

---

## 1. Three.js 核心初始化

### 1.1 ES Module 方式（推荐）

```js
// importmap 方式 — 无需打包工具
<script type="importmap">
{
  "imports": {
    "three": "https://unpkg.com/three@0.170.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.170.0/examples/jsm/"
  }
}
</script>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
</script>
```

### 1.2 React Three Fiber (R3F) + Next.js

```tsx
// components/Scene.tsx
'use client';

import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import { Suspense, useRef } from 'react';
import * as THREE from 'three';

function Scene() {
  const meshRef = useRef<THREE.Mesh>(null);

  return (
    <Canvas
      dpr={[1, 2]}
      gl={{
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance',
      }}
      camera={{ position: [0, 0, 5], fov: 45 }}
    >
      <Suspense fallback={null}>
        {/* 灯光 */}
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 5, 5]} intensity={1} />

        {/* 3D 对象 */}
        <mesh ref={meshRef}>
          <sphereGeometry args={[1, 64, 64]} />
          <meshStandardMaterial color="#4488ff" roughness={0.3} metalness={0.8} />
        </mesh>

        {/* 环境贴图 */}
        <Environment preset="city" />

        {/* 控制器 */}
        <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
      </Suspense>
    </Canvas>
  );
}

export default function Page() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <Scene />
    </div>
  );
}
```

### 1.3 渲染器配置与像素比限制

```js
const renderer = new THREE.WebGLRenderer({
  antialias: true,
  alpha: true,
  powerPreference: 'high-performance', // 优先使用独立 GPU
});

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // ⚠️ 关键：限制 dpr 防止移动端卡顿
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  45,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.set(0, 0, 5);
```

### 1.4 响应式缩放处理

```js
function onResize() {
  const width = window.innerWidth;
  const height = window.innerHeight;

  camera.aspect = width / height;
  camera.updateProjectionMatrix();

  renderer.setSize(width, height);
  // 像素比也需要重新计算（用户可能在多显示器间拖动窗口）
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
}

window.addEventListener('resize', onResize);

// 如果使用 ResizeObserver 监听容器（非全屏场景）
const ro = new ResizeObserver((entries) => {
  for (const entry of entries) {
    const { width, height } = entry.contentRect;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  }
});
ro.observe(document.getElementById('canvas-container'));
```

---

## 2. 粒子系统

### 2.1 星空背景（最稳定方案）

> Awwwards 网站中使用率最高的 WebGL 效果，几乎零成本、高视觉回报。

```js
function createStarField(count = 2000, spread = 50) {
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(count * 3);
  const sizes = new Float32Array(count);

  for (let i = 0; i < count; i++) {
    positions[i * 3]     = (Math.random() - 0.5) * spread;
    positions[i * 3 + 1] = (Math.random() - 0.5) * spread;
    positions[i * 3 + 2] = (Math.random() - 0.5) * spread;
    sizes[i] = Math.random() * 2 + 0.5;
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('aSize', new THREE.BufferAttribute(sizes, 1));

  const material = new THREE.ShaderMaterial({
    uniforms: {
      uTime:  { value: 0 },
      uColor: { value: new THREE.Color('#ffffff') },
    },
    vertexShader: `
      attribute float aSize;
      uniform float uTime;
      varying float vAlpha;

      void main() {
        vec4 mvPos = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = aSize * (300.0 / -mvPos.z);
        gl_Position = projectionMatrix * mvPos;

        // 闪烁效果
        vAlpha = 0.4 + 0.6 * sin(uTime * 0.5 + position.x * 10.0);
      }
    `,
    fragmentShader: `
      uniform vec3 uColor;
      varying float vAlpha;

      void main() {
        // 圆形粒子 + 柔和边缘
        float dist = length(gl_PointCoord - 0.5);
        if (dist > 0.5) discard;
        float alpha = smoothstep(0.5, 0.1, dist) * vAlpha;
        gl_FragColor = vec4(uColor, alpha);
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });

  const points = new THREE.Points(geometry, material);
  return { points, material };
}

// 使用
const { points, material } = createStarField();
scene.add(points);

function animate() {
  requestAnimationFrame(animate);
  material.uniforms.uTime.value += 0.01;
  points.rotation.y += 0.0002;
  renderer.render(scene, camera);
}
animate();
```

### 2.2 自定义粒子形状

```js
// 使用 Canvas 动态生成粒子贴图
function createParticleTexture() {
  const canvas = document.createElement('canvas');
  canvas.width = 64;
  canvas.height = 64;
  const ctx = canvas.getContext('2d');

  // 径向渐变 → 柔和光点
  const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
  gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
  gradient.addColorStop(0.3, 'rgba(255, 255, 255, 0.6)');
  gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 64, 64);

  const texture = new THREE.CanvasTexture(canvas);
  return texture;
}

// 也可以用 SpriteMaterial 替代 Points（适合少量大粒子）
const spriteMap = createParticleTexture();
const spriteMat = new THREE.SpriteMaterial({
  map: spriteMap,
  color: 0x4488ff,
  transparent: true,
  blending: THREE.AdditiveBlending,
});
const sprite = new THREE.Sprite(spriteMat);
sprite.scale.set(0.5, 0.5, 1);
scene.add(sprite);
```

### 2.3 GPU 粒子系统 — 颜色渐变

```js
function createGradientParticles(count = 5000) {
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const velocities = new Float32Array(count * 3); // JS 端存储速度

  const colorStart = new THREE.Color('#ff3366'); // 粉红
  const colorEnd = new THREE.Color('#3366ff');   // 蓝紫

  for (let i = 0; i < count; i++) {
    // 球形分布
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const r = 2 + Math.random() * 3;

    positions[i * 3]     = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = r * Math.cos(phi);

    // 根据距离中心的远近混合颜色
    const t = r / 5; // 0~1
    const c = colorStart.clone().lerp(colorEnd, t);
    colors[i * 3]     = c.r;
    colors[i * 3 + 1] = c.g;
    colors[i * 3 + 2] = c.b;

    velocities[i * 3]     = (Math.random() - 0.5) * 0.01;
    velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.01;
    velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.01;
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('aColor', new THREE.BufferAttribute(colors, 3));

  const material = new THREE.ShaderMaterial({
    vertexShader: `
      attribute vec3 aColor;
      varying vec3 vColor;

      void main() {
        vColor = aColor;
        vec4 mvPos = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = 3.0 * (200.0 / -mvPos.z);
        gl_Position = projectionMatrix * mvPos;
      }
    `,
    fragmentShader: `
      varying vec3 vColor;

      void main() {
        float d = length(gl_PointCoord - 0.5);
        if (d > 0.5) discard;
        float a = smoothstep(0.5, 0.0, d);
        gl_FragColor = vec4(vColor, a * 0.8);
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });

  return new THREE.Points(geometry, material);
}
```

---

## 3. 流体/有机形态

### 3.1 流体球体 — 顶点变形

```js
const sphereGeo = new THREE.SphereGeometry(1, 128, 128);
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime:  { value: 0 },
    uNoise: { value: null }, // NoiseTexture
  },
  vertexShader: `
    uniform float uTime;

    // Simplex 3D 噪声（GLSL 内联实现）
    vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
    vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
    vec4 permute(vec4 x) { return mod289(((x * 34.0) + 10.0) * x); }
    vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

    float snoise(vec3 v) {
      const vec2 C = vec2(1.0/6.0, 1.0/3.0);
      const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);

      vec3 i  = floor(v + dot(v, C.yyy));
      vec3 x0 = v - i + dot(i, C.xxx);

      vec3 g = step(x0.yzx, x0.xyz);
      vec3 l = 1.0 - g;
      vec3 i1 = min(g.xyz, l.zxy);
      vec3 i2 = max(g.xyz, l.zxy);

      vec3 x1 = x0 - i1 + C.xxx;
      vec3 x2 = x0 - i2 + C.yyy;
      vec3 x3 = x0 - D.yyy;

      i = mod289(i);
      vec4 p = permute(permute(permute(
        i.z + vec4(0.0, i1.z, i2.z, 1.0))
        + i.y + vec4(0.0, i1.y, i2.y, 1.0))
        + i.x + vec4(0.0, i1.x, i2.x, 1.0));

      float n_ = 0.142857142857;
      vec3 ns = n_ * D.wyz - D.xzx;

      vec4 j = p - 49.0 * floor(p * ns.z * ns.z);

      vec4 x_ = floor(j * ns.z);
      vec4 y_ = floor(j - 7.0 * x_);

      vec4 x = x_ * ns.x + ns.yyyy;
      vec4 y = y_ * ns.x + ns.yyyy;
      vec4 h = 1.0 - abs(x) - abs(y);

      vec4 b0 = vec4(x.xy, y.xy);
      vec4 b1 = vec4(x.zw, y.zw);

      vec4 s0 = floor(b0) * 2.0 + 1.0;
      vec4 s1 = floor(b1) * 2.0 + 1.0;
      vec4 sh = -step(h, vec4(0.0));

      vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
      vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;

      vec3 p0 = vec3(a0.xy, h.x);
      vec3 p1 = vec3(a0.zw, h.y);
      vec3 p2 = vec3(a1.xy, h.z);
      vec3 p3 = vec3(a1.zw, h.w);

      vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
      p0 *= norm.x;
      p1 *= norm.y;
      p2 *= norm.z;
      p3 *= norm.w;

      vec4 m = max(0.5 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
      m = m * m;
      return 105.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
    }

    varying vec3 vNormal;
    varying vec3 vPosition;
    varying float vDisplacement;

    void main() {
      float noise = snoise(position * 1.5 + uTime * 0.3);
      float displacement = noise * 0.3;
      vec3 newPos = position + normal * displacement;

      vNormal = normalMatrix * normal;
      vPosition = (modelViewMatrix * vec4(newPos, 1.0)).xyz;
      vDisplacement = displacement;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(newPos, 1.0);
    }
  `,
  fragmentShader: `
    varying vec3 vNormal;
    varying vec3 vPosition;
    varying float vDisplacement;

    void main() {
      // 基于位移量的颜色渐变：蓝 → 粉
      vec3 color1 = vec3(0.2, 0.4, 1.0);
      vec3 color2 = vec3(1.0, 0.3, 0.5);
      vec3 baseColor = mix(color1, color2, vDisplacement * 2.0 + 0.5);

      // 简单的 Fresnel 效果
      vec3 viewDir = normalize(-vPosition);
      float fresnel = pow(1.0 - max(dot(normalize(vNormal), viewDir), 0.0), 3.0);

      vec3 finalColor = baseColor + fresnel * vec3(0.3, 0.5, 1.0) * 0.5;
      gl_FragColor = vec4(finalColor, 1.0);
    }
  `,
});

const fluidSphere = new THREE.Mesh(sphereGeo, material);
scene.add(fluidSphere);
```

### 3.2 Metaballs（融合球体效果）

```js
// 使用 MarchingCubes 实现 metaball 融合效果
import { MarchingCubes } from 'three/addons/objects/MarchingCubes.js';

const resolution = 48; // 越高越精细，性能开销越大
const material = new THREE.MeshStandardMaterial({
  color: 0x4488ff,
  roughness: 0.2,
  metalness: 0.8,
  transparent: true,
  opacity: 0.9,
});

const effect = new MarchingCubes(resolution, material, true, true, 100000);
effect.position.set(0, 0, 0);
effect.scale.set(3, 3, 3);
scene.add(effect);

// 在动画循环中更新 metaball 位置
function updateMetaballs(time) {
  effect.reset();

  // 添加多个运动的球体
  const ballCount = 5;
  for (let i = 0; i < ballCount; i++) {
    const t = time * 0.5 + i * (Math.PI * 2 / ballCount);
    effect.addBall(
      Math.sin(t) * 0.5,       // x
      Math.cos(t * 0.7) * 0.5, // y
      Math.sin(t * 0.5) * 0.5, // z
      0.6,                       // 半径
      12                         // 强度
    );
  }
}
```

### 3.3 Blob 形状 — CatmullRomCurve3

```js
function createBlobShape() {
  const points = [];
  const segments = 8;

  for (let i = 0; i <= segments; i++) {
    const angle = (i / segments) * Math.PI * 2;
    const radius = 1 + Math.sin(angle * 3) * 0.3 + Math.cos(angle * 2) * 0.2;
    points.push(new THREE.Vector3(
      Math.cos(angle) * radius,
      Math.sin(angle) * radius,
      Math.sin(angle * 2) * 0.5
    ));
  }

  const curve = new THREE.CatmullRomCurve3(points, true);
  const geometry = new THREE.TubeGeometry(curve, 100, 0.15, 16, true);
  const material = new THREE.MeshPhysicalMaterial({
    color: 0xff4488,
    roughness: 0.1,
    metalness: 0.5,
    clearcoat: 1.0,
    clearcoatRoughness: 0.1,
  });

  return new THREE.Mesh(geometry, material);
}
```

---

## 4. GLSL 着色器特效

### 4.1 自定义 ShaderMaterial 标准模板

```js
// ⚠️ 重要：永远不要使用 Three.js 内置属性名
// 错误: attribute vec3 color, attribute vec3 normal → 使用 aColor, aNormal
const shaderMaterial = new THREE.ShaderMaterial({
  uniforms: {
    uTime:       { value: 0 },
    uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
    uMouse:      { value: new THREE.Vector2(0, 0) },
    uTexture:    { value: null },
    uOpacity:    { value: 1.0 },
  },
  vertexShader: `
    uniform float uTime;
    varying vec2 vUv;

    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform vec2 uResolution;
    uniform vec2 uMouse;
    uniform sampler2D uTexture;
    varying vec2 vUv;

    void main() {
      vec4 texColor = texture2D(uTexture, vUv);
      gl_FragColor = texColor;
    }
  `,
  transparent: true,
  side: THREE.DoubleSide,
});
```

### 4.2 鼠标跟随光效

```glsl
// 在 fragment shader 中添加鼠标光晕
uniform vec2 uMouse;
varying vec2 vUv;

void main() {
  vec2 mousePos = uMouse;
  float dist = distance(vUv, mousePos);
  float glow = exp(-dist * 5.0) * 0.6; // 高斯衰减

  vec3 glowColor = vec3(0.4, 0.6, 1.0);
  vec3 baseColor = texture2D(uTexture, vUv).rgb;

  vec3 finalColor = baseColor + glowColor * glow;
  gl_FragColor = vec4(finalColor, 1.0);
}
```

```js
// JS 端：监听鼠标并传递 uniform
const mouse = new THREE.Vector2();
window.addEventListener('mousemove', (e) => {
  mouse.x = e.clientX / window.innerWidth;
  mouse.y = 1.0 - e.clientY / window.innerHeight;
  shaderMaterial.uniforms.uMouse.value.set(mouse.x, mouse.y);
});
```

### 4.3 后处理管线（Bloom + 色差 + 噪点）

```js
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';

// 1. 基础渲染通道
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));

// 2. Bloom 辉光
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  0.8,   // 强度
  0.4,   // 半径
  0.85   // 阈值 — 越低越多元素发光
);
composer.addPass(bloomPass);

// 3. 色差 + 噪点（自定义后处理 shader）
const chromaticAberrationShader = {
  uniforms: {
    tDiffuse:     { value: null },
    uTime:        { value: 0 },
    uStrength:    { value: 0.003 }, // 色差强度
    uGrainAmount: { value: 0.04 },  // 噪点强度
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float uTime;
    uniform float uStrength;
    uniform float uGrainAmount;
    varying vec2 vUv;

    // 伪随机函数
    float random(vec2 st) {
      return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453);
    }

    void main() {
      // 色差：偏移 R/B 通道
      vec2 dir = vUv - 0.5;
      float dist = length(dir);

      float r = texture2D(tDiffuse, vUv + dir * uStrength).r;
      float g = texture2D(tDiffuse, vUv).g;
      float b = texture2D(tDiffuse, vUv - dir * uStrength).b;

      vec3 color = vec3(r, g, b);

      // 胶片噪点
      float grain = random(vUv * uTime) * uGrainAmount;
      color += grain;

      // 暗角
      color *= 1.0 - dist * 0.4;

      gl_FragColor = vec4(color, 1.0);
    }
  `,
};

const customPass = new ShaderPass(chromaticAberrationShader);
composer.addPass(customPass);

// 动画循环中使用 composer.render() 替代 renderer.render()
function animate() {
  requestAnimationFrame(animate);
  customPass.uniforms.uTime.value += 0.01;
  composer.render();
}
```

### 4.4 Raymarching — SDF 场景

```glsl
// 完整的 Raymarching fragment shader
uniform float uTime;
uniform vec2 uResolution;

// 旋转矩阵
mat2 rotate2D(float a) {
  float s = sin(a), c = cos(a);
  return mat2(c, -s, s, c);
}

// SDF 原始形状
float sdSphere(vec3 p, float r) { return length(p) - r; }

float sdBox(vec3 p, vec3 b) {
  vec3 q = abs(p) - b;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

float sdTorus(vec3 p, vec2 t) {
  vec2 q = vec2(length(p.xz) - t.x, p.y);
  return length(q) - t.y;
}

// 场景 SDF：多个形状的组合
float sceneSDF(vec3 p) {
  p.xz *= rotate2D(uTime * 0.3);
  p.xy *= rotate2D(uTime * 0.2);

  float sphere = sdSphere(p, 1.0);
  float box = sdBox(p, vec3(0.7));

  // 平滑并集 (Smooth Union)
  float blend = 0.8;
  float d = sphere + box - blend;
  d = max(sphere, max(box, d + blend));

  return d - sin(p.x * 5.0 + uTime) * 0.05; // 表面波纹
}

// 法线计算（中心差分法）
vec3 calcNormal(vec3 p) {
  vec2 e = vec2(0.001, 0.0);
  return normalize(vec3(
    sceneSDF(p + e.xyy) - sceneSDF(p - e.xyy),
    sceneSDF(p + e.yxy) - sceneSDF(p - e.yxy),
    sceneSDF(p + e.yyx) - sceneSDF(p - e.yyx)
  ));
}

void main() {
  vec2 uv = (gl_FragCoord.xy - 0.5 * uResolution) / min(uResolution.x, uResolution.y);

  // 相机
  vec3 ro = vec3(0.0, 0.0, 3.0); // 射线起点
  vec3 rd = normalize(vec3(uv, -1.5)); // 射线方向

  // Raymarching
  float t = 0.0;
  for (int i = 0; i < 80; i++) {
    vec3 p = ro + rd * t;
    float d = sceneSDF(p);
    if (d < 0.001) break;
    if (t > 100.0) break;
    t += d;
  }

  vec3 color = vec3(0.02, 0.02, 0.05); // 背景色

  if (t < 100.0) {
    vec3 p = ro + rd * t;
    vec3 n = calcNormal(p);
    vec3 lightDir = normalize(vec3(1.0, 1.0, -1.0));

    // 漫反射 + 镜面反射
    float diff = max(dot(n, lightDir), 0.0);
    vec3 viewDir = normalize(ro - p);
    vec3 halfDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(n, halfDir), 0.0), 32.0);

    vec3 baseColor = mix(vec3(0.2, 0.4, 1.0), vec3(1.0, 0.3, 0.5),
                         sin(p.y * 3.0 + uTime) * 0.5 + 0.5);

    color = baseColor * (diff * 0.8 + 0.2) + vec3(1.0) * spec * 0.5;
  }

  // Gamma 校正
  color = pow(color, vec3(1.0 / 2.2));

  gl_FragColor = vec4(color, 1.0);
}
```

### 4.5 渐变颜色混合技巧

```glsl
// 方法1: 线性插值
vec3 gradient1 = mix(colorA, colorB, t);

// 方法2: 多色渐变（色带）
vec3 multiGradient(float t) {
  vec3 c1 = vec3(0.94, 0.25, 0.35); // #F04059
  vec3 c2 = vec3(0.97, 0.58, 0.20); // #F79433
  vec3 c3 = vec3(0.20, 0.73, 0.89); // #33BAE3

  t = clamp(t, 0.0, 1.0);
  if (t < 0.5) return mix(c1, c2, t * 2.0);
  return mix(c2, c3, (t - 0.5) * 2.0);
}

// 方法3: 余弦调色板 (IQ palette) — 最常用
vec3 palette(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
  return a + b * cos(6.28318 * (c * t + d));
}

// Awwwards 常用参数组合
vec3 awwwardsPalette(float t) {
  // 蓝紫渐变
  return palette(t,
    vec3(0.5, 0.5, 0.5),
    vec3(0.5, 0.5, 0.5),
    vec3(1.0, 1.0, 1.0),
    vec3(0.0, 0.10, 0.20)
  );
  // 粉蓝渐变 → d 参数改为 vec3(0.0, 0.33, 0.67)
  // 火焰渐变 → d 参数改为 vec3(0.0, 0.10, 0.20)
}
```

---

## 5. WebGL 性能优化

### 5.1 Intersection Observer 懒初始化

```js
// 只在 WebGL canvas 进入视口时初始化
class LazyWebGL {
  constructor(containerEl, createSceneFn) {
    this.container = containerEl;
    this.createScene = createSceneFn;
    this.initialized = false;
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !this.initialized) {
            this.init();
          }
          // 离开视口时暂停渲染（节省 CPU/GPU）
          if (!entry.isIntersecting && this.initialized) {
            this.pause();
          }
          if (entry.isIntersecting && this.initialized) {
            this.resume();
          }
        });
      },
      { threshold: 0.1 }
    );
    this.observer.observe(containerEl);
  }

  init() {
    this.initialized = true;
    const { renderer, scene, camera, animate } = this.createScene(this.container);
    this.renderer = renderer;
    this.scene = scene;
    this.camera = camera;
    this.animate = animate;
    this.animate();
  }

  pause() {
    this.running = false;
  }

  resume() {
    if (!this.running) {
      this.running = true;
      this.animate();
    }
  }
}

// 使用
new LazyWebGL(document.getElementById('webgl-container'), (container) => {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
  camera.position.z = 5;

  // ... 添加场景内容 ...

  function animate() {
    if (!this.running) return; // 用闭包或类的属性控制
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }

  return { renderer, scene, camera, animate };
});
```

### 5.2 GPU 等级检测 + 质量分级

```js
import { getGPUTier } from 'detect-gpu';

async function getQualitySettings() {
  const gpuTier = await getGPUTier();
  const isMobile = /Android|iPhone|iPad/i.test(navigator.userAgent);

  // 根据设备能力返回质量参数
  if (isMobile || gpuTier.tier < 2) {
    return {
      particleCount: 1000,      // 移动端/低端 GPU
      pixelRatio: 1,
      shadowMap: false,
      postProcessing: false,
      textureSize: 512,
    };
  }

  if (gpuTier.tier < 3) {
    return {
      particleCount: 3000,      // 中端 GPU
      pixelRatio: 1.5,
      shadowMap: true,
      postProcessing: 'low',
      textureSize: 1024,
    };
  }

  return {
    particleCount: 8000,        // 高端 GPU
    pixelRatio: 2,
    shadowMap: true,
    postProcessing: 'high',
    textureSize: 2048,
  };
}
```

### 5.3 资源释放（内存泄漏防护）

```js
function disposeScene(scene, renderer) {
  scene.traverse((object) => {
    if (object.geometry) {
      object.geometry.dispose();
    }
    if (object.material) {
      // 材质可能是一个数组（多材质）
      const materials = Array.isArray(object.material)
        ? object.material
        : [object.material];

      materials.forEach((mat) => {
        // 释放所有纹理
        Object.values(mat.uniforms || {}).forEach((uniform) => {
          if (uniform.value && uniform.value.isTexture) {
            uniform.value.dispose();
          }
        });
        // 释放材质的贴图
        if (mat.map) mat.map.dispose();
        if (mat.normalMap) mat.normalMap.dispose();
        if (mat.roughnessMap) mat.roughnessMap.dispose();
        if (mat.metalnessMap) mat.metalnessMap.dispose();

        mat.dispose();
      });
    }
  });

  renderer.dispose();
  renderer.forceContextLoss(); // 强制释放 WebGL 上下文
}

// React 中的清理函数
useEffect(() => {
  // ... 初始化 ...

  return () => {
    disposeScene(scene, renderer);
  };
}, []);
```

### 5.4 OffscreenCanvas 重计算

```js
// 在 Web Worker 中运行 OffscreenCanvas，避免阻塞主线程
// main.js
const canvas = document.getElementById('webgl-canvas');
const offscreen = canvas.transferControlToOffscreen();
const worker = new Worker('webgl-worker.js');
worker.postMessage({ canvas: offscreen }, [offscreen]);

// webgl-worker.js
import * as THREE from 'three';

let scene, camera, renderer;

self.onmessage = (e) => {
  if (e.data.canvas) {
    const canvas = e.data.canvas;
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    // ... 场景初始化 ...
    animate();
  }
};

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
```

---

## 6. WebGPU（2026 下一代）

### 概述

| 特性 | WebGL 2 | WebGPU |
|------|---------|--------|
| 计算着色器 | ❌ | ✅ Compute Shader |
| 着色语言 | GLSL | WGSL |
| 管线控制 | 固定管线 | 可编程渲染管线 |
| 多线程 | 有限 | 原生支持 |
| 性能 | 好 | 显著提升 (2-5x) |
| API 风格 | OpenGL 风格 | 现代 Vulkan/Metal 风格 |

### 何时使用 WebGPU

- **大规模粒子系统**（10万+）：Compute Shader 并行计算粒子位置
- **实时光线追踪**：WebGPU 的 Ray Tracing 扩展
- **复杂物理模拟**：GPU 端物理计算
- **AI/ML 推理**：WebNN + WebGPU 协同

### 浏览器支持（2025年中）

- ✅ Chrome 113+
- ✅ Edge 113+
- ✅ Firefox Nightly（实验性）
- ✅ Safari 18+（部分支持）
- ❌ 移动端：仅 Chrome Android

### Three.js 中使用 WebGPU

```js
import WebGPURenderer from 'three/addons/renderers/webgpu/WebGPURenderer.js';

async function initWebGPU() {
  // 检测 WebGPU 是否可用
  if (!navigator.gpu) {
    console.warn('WebGPU 不可用，回退到 WebGL');
    return initWebGL(); // 降级方案
  }

  const renderer = new WebGPURenderer({ antialias: true });
  await renderer.init(); // WebGPU 需要异步初始化

  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // 之后用法与 WebGLRenderer 基本一致
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
  camera.position.z = 5;

  return { renderer, scene, camera };
}
```

### WGSL 着色器示例

```wgsl
// WebGPU 使用 WGSL (WebGPU Shading Language) 替代 GLSL
// 注意语法差异

struct Uniforms {
  time: f32,
  resolution: vec2<f32>,
};

@group(0) @binding(0) var<uniform> u: Uniforms;

@vertex
fn vertexMain(@location(0) position: vec3<f32>) -> @builtin(position) vec4<f32> {
  return vec4<f32>(position, 1.0);
}

@fragment
fn fragmentMain(@builtin(position) fragCoord: vec4<f32>) -> @location(0) vec4<f32> {
  let uv = fragCoord.xy / u.resolution;
  let color = vec3<f32>(uv.x, uv.y, sin(u.time) * 0.5 + 0.5);
  return vec4<f32>(color, 1.0);
}
```

> **建议**：2025-2026 年大多数 Awwwards 网站仍以 Three.js + WebGL 为主。WebGPU 适合实验性项目或需要极致性能的场景。始终提供 WebGL 降级方案。

---

## 7. 3D 资产管线

### 7.1 Blender → glTF → Three.js

```bash
# Blender 导出设置（File → Export → glTF 2.0）
# ✅ Format: glTF Binary (.glb)
# ✅ Include: Selected Objects Only
# ✅ Transform: +Y Up
# ✅ Geometry: Apply Modifiers ✅, Compression: Draco
# ✅ Materials: Export Materials ✅

# Draco 压缩（减小模型体积 70-90%）
npm install -g gltf-pipeline
gltf-pipeline -i model.glb -o model-compressed.glb --draco.compressionLevel 7
```

```js
// Three.js 加载 glTF
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

gltfLoader.load(
  '/models/hero-model.glb',
  (gltf) => {
    const model = gltf.scene;

    // 自动缩放到合适大小
    const box = new THREE.Box3().setFromObject(model);
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const scale = 2 / maxDim;
    model.scale.setScalar(scale);

    // 居中
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center.multiplyScalar(scale));

    scene.add(model);
  },
  (progress) => {
    console.log(`Loading: ${(progress.loaded / progress.total * 100).toFixed(0)}%`);
  },
  (error) => {
    console.error('Model loading failed:', error);
  }
);
```

### 7.2 Spline — 无代码 3D 场景

```js
// 从 Spline 导出嵌入代码
// 方法1: 使用 @splinetool/react-spline（推荐）
import Spline from '@splinetool/react-spline';

function HeroSection() {
  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <Spline scene="https://prod.spline.design/YOUR_SCENE_ID/scene.splinecode" />
    </div>
  );
}

// 方法2: 直接加载 Spline Runtime
import { Application } from '@splinetool/runtime';

const app = new Application(canvas);
await app.load('https://prod.spline.design/YOUR_SCENE_ID/scene.splinecode');

// 获取场景中的对象进行交互
const obj = app.findObjectByName('MySphere');
obj.emitEvent('mouseHover');
```

### 7.3 纹理优化

```bash
# 纹理压缩工具
npm install -g gltf-transform

# 压缩纹理为 WebP（比 PNG 小 30%）
gltf-transform resize model.glb output.glb --width 1024 --height 1024

# 使用 Basis Universal 压缩（GPU 直接解码，零运行时开销）
gltf-transform etc1s model.glb output.glb --quality 75

# 或使用 KTX2 格式
gltf-transform ktx2 model.glb output.glb --slots diffuse,normalMap,orm
```

```js
// Three.js 加载 KTX2 纹理
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('https://unpkg.com/three@0.170.0/examples/jsm/libs/basis/');
ktx2Loader.detectSupport(renderer);
```

### 7.4 模型面数目标

| 用途 | 面数上限 | 备注 |
|------|---------|------|
| 英雄区 3D 展示 | 50K-200K | 用 Draco 压缩后 < 5MB |
| 全屏背景模型 | 10K-50K | 简化几何体 |
| 图标/小装饰 | < 5K | 可以用更多 |
| 移动端 | < 30K | 必须精简 |
| 粒子/点云 | N/A | 用 BufferGeometry 而非 Mesh |

---

## 8. 鼠标/滚动交互

### 8.1 鼠标跟随相机运动

```js
const mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };

window.addEventListener('mousemove', (e) => {
  mouse.targetX = (e.clientX / window.innerWidth - 0.5) * 2;
  mouse.targetY = (e.clientY / window.innerHeight - 0.5) * 2;
});

function animate() {
  requestAnimationFrame(animate);

  // 平滑插值（lerp），避免生硬跳动
  mouse.x += (mouse.targetX - mouse.x) * 0.05;
  mouse.y += (mouse.targetY - mouse.y) * 0.05;

  // 相机微妙偏移（视差效果）
  camera.position.x = mouse.x * 0.5;
  camera.position.y = -mouse.y * 0.3;
  camera.lookAt(scene.position); // 始终看向场景中心

  renderer.render(scene, camera);
}
```

### 8.2 滚动联动相机位移

```js
import { Lenis } from 'lenis'; // 推荐：平滑滚动库

const lenis = new Lenis({
  lerp: 0.1,         // 滚动平滑度
  smoothWheel: true,  // 平滑滚轮
});

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

// 监听滚动进度
let scrollProgress = 0;

lenis.on('scroll', ({ progress }) => {
  scrollProgress = progress; // 0 → 1
});

// 在动画循环中使用
function animate() {
  requestAnimationFrame(animate);

  // 相机沿 Z 轴推进
  camera.position.z = 10 - scrollProgress * 8;

  // 或沿路径移动
  const path = new THREE.LineCurve3(
    new THREE.Vector3(0, 0, 5),
    new THREE.Vector3(0, -3, 15)
  );
  const point = path.getPoint(scrollProgress);
  camera.position.copy(point);
  camera.lookAt(new THREE.Vector3(0, -3, 15));

  renderer.render(scene, camera);
}
```

### 8.3 滚动联动动画进度

```js
// GSAP ScrollTrigger + Three.js（Awwwards 最常用组合）
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const uniforms = {
  uProgress: { value: 0 }, // 0 → 1 动画进度
};

gsap.to(uniforms.uProgress, {
  value: 1,
  scrollTrigger: {
    trigger: '#webgl-section',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 1, // 平滑绑定滚动
  },
});

// 在 shader 中使用 uProgress
const material = new THREE.ShaderMaterial({
  uniforms,
  vertexShader: `
    uniform float uProgress;
    void main() {
      vec3 pos = position;
      // 根据滚动进度旋转
      float angle = uProgress * 3.14159;
      pos.xz = mat2(cos(angle), -sin(angle), sin(angle), cos(angle)) * pos.xz;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  fragmentShader: `
    uniform float uProgress;
    void main() {
      vec3 color = mix(vec3(0.2, 0.4, 1.0), vec3(1.0, 0.3, 0.5), uProgress);
      gl_FragColor = vec4(color, 1.0);
    }
  `,
});
```

### 8.4 光线投射 — 鼠标与 3D 物体交互

```js
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
let hoveredObject = null;

window.addEventListener('mousemove', (e) => {
  pointer.x = (e.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(e.clientY / window.innerHeight) * 2 + 1;
});

window.addEventListener('click', () => {
  if (hoveredObject) {
    // 点击处理
    console.log('Clicked:', hoveredObject.name);

    // 弹跳动画
    gsap.to(hoveredObject.scale, {
      x: 1.2, y: 1.2, z: 1.2,
      duration: 0.3,
      yoyo: true,
      repeat: 1,
      ease: 'elastic.out(1, 0.3)',
    });
  }
});

function animate() {
  requestAnimationFrame(animate);

  // 射线投射检测
  raycaster.setFromCamera(pointer, camera);
  const intersects = raycaster.intersectObjects(interactiveObjects);

  if (intersects.length > 0) {
    const obj = intersects[0].object;

    if (hoveredObject !== obj) {
      // 恢复上一个悬停对象
      if (hoveredObject) {
        hoveredObject.material.emissive?.setHex(0x000000);
      }

      // 高亮新对象
      hoveredObject = obj;
      hoveredObject.material.emissive?.setHex(0x333333);
      document.body.style.cursor = 'pointer';
    }
  } else {
    if (hoveredObject) {
      hoveredObject.material.emissive?.setHex(0x000000);
      hoveredObject = null;
      document.body.style.cursor = 'default';
    }
  }

  renderer.render(scene, camera);
}
```

### 8.5 完整的滚动视差示例（GSAP + R3F）

```tsx
'use client';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { useRef, useEffect } from 'react';
import { MotionPathPlugin, ScrollTrigger } from 'gsap/all';
import gsap from 'gsap';

gsap.registerPlugin(MotionPathPlugin, ScrollTrigger);

function ScrollLinkedMesh() {
  const meshRef = useRef<THREE.Mesh>(null);
  const progressRef = useRef(0);

  useEffect(() => {
    // 绑定滚动到 ref
    ScrollTrigger.create({
      trigger: 'body',
      start: 'top top',
      end: 'bottom bottom',
      onUpdate: (self) => {
        progressRef.current = self.progress;
      },
    });
  }, []);

  useFrame(() => {
    if (!meshRef.current) return;
    const p = progressRef.current;

    meshRef.current.rotation.x = p * Math.PI * 4;
    meshRef.current.rotation.y = p * Math.PI * 2;
    meshRef.current.position.y = Math.sin(p * Math.PI * 3) * 0.5;
    meshRef.current.scale.setScalar(1 + Math.sin(p * Math.PI) * 0.3);
  });

  return (
    <mesh ref={meshRef}>
      <icosahedronGeometry args={[1, 4]} />
      <meshPhysicalMaterial
        color="#4488ff"
        roughness={0.1}
        metalness={0.9}
        clearcoat={1}
      />
    </mesh>
  );
}

export default function ParallaxPage() {
  return (
    <>
      {/* 足够长的滚动空间 */}
      <div style={{ height: '500vh', background: '#000', position: 'relative' }}>
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100vh' }}>
          <Canvas
            dpr={[1, 2]}
            gl={{ antialias: true, alpha: true }}
            camera={{ position: [0, 0, 5], fov: 45 }}
          >
            <ambientLight intensity={0.3} />
            <pointLight position={[5, 5, 5]} intensity={1} />
            <ScrollLinkedMesh />
          </Canvas>
        </div>

        {/* 滚动内容覆盖层 */}
        <div style={{ position: 'relative', zIndex: 1, pointerEvents: 'none' }}>
          <section style={{ height: '100vh' }} />
          <section style={{ height: '100vh' }}>
            <h1 style={{ color: 'white', fontSize: '4rem', textAlign: 'center' }}>
              Scroll to Transform
            </h1>
          </section>
          <section style={{ height: '100vh' }} />
        </div>
      </div>
    </>
  );
}
```

---

## 附录：常用工具与资源

| 工具 | 用途 |
|------|------|
| [Three.js](https://threejs.org/) | 核心渲染库 |
| [React Three Fiber](https://docs.pmnd.rs/react-three-fiber) | React 3D 框架 |
| [Drei](https://docs.pmnd.rs/drei) | R3F 常用辅助组件 |
| [GSAP](https://gsap.com/) | 动画引擎 + ScrollTrigger |
| [Lenis](https://github.com/darkroomengineering/lenis) | 平滑滚动 |
| [detect-gpu](https://github.com/nicejam/detect-gpu) | GPU 等级检测 |
| [gltf-transform](https://gltf-transform.donmccurdy.com/) | glTF 模型优化 |
| [Spline](https://spline.design/) | 无代码 3D 设计 |
| [glTF Viewer](https://gltf-viewer.donmccurdy.com/) | 模型预览 |
| [Shadertoy](https://www.shadertoy.com/) | GLSL 着色器灵感 |
| [The Book of Shaders](https://thebookofshaders.com/) | GLSL 入门教程 |

---

## 最佳实践清单

- [ ] ✅ 始终限制 `devicePixelRatio` 为 `Math.min(dpr, 2)`
- [ ] ✅ ShaderMaterial 中避免使用 Three.js 内置属性名（`color` → `aColor`）
- [ ] ✅ 使用 `IntersectionObserver` 延迟初始化非首屏 WebGL
- [ ] ✅ 粒子系统使用 `AdditiveBlending` + `depthWrite: false`
- [ ] ✅ 离屏时暂停渲染循环
- [ ] ✅ 组件卸载时释放所有 geometry、material、texture
- [ ] ✅ 提供移动端降级方案（减少粒子数、关闭后处理）
- [ ] ✅ 模型使用 Draco 压缩 + 纹理使用 Basis/KTX2
- [ ] ✅ 鼠标跟随使用 lerp 平滑插值
- [ ] ✅ 滚动动画使用 `scrub` 绑定而非实时监听
