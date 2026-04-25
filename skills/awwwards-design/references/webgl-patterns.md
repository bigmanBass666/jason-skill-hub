# WebGL / Three.js 实现模式

## 模式1：粒子星空背景（最稳健）

```javascript
function createParticleField(scene) {
  const count = 2000;
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  
  for (let i = 0; i < count; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 20;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
    
    // 渐变色粒子
    const t = Math.random();
    colors[i * 3] = 0.2 + t * 0.8;      // R
    colors[i * 3 + 1] = 0.1 + t * 0.3;  // G
    colors[i * 3 + 2] = 0.8 - t * 0.3;  // B
  }
  
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  
  const mat = new THREE.PointsMaterial({
    size: 0.02,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    sizeAttenuation: true,
  });
  
  return new THREE.Points(geo, mat);
}
```

## 模式2：流体球体（有机感）

```javascript
function createFluidSphere(scene) {
  const geo = new THREE.SphereGeometry(1.5, 64, 64);
  
  // 保存原始顶点
  const posAttr = geo.attributes.position;
  const originalPos = posAttr.array.slice();
  
  const mat = new THREE.MeshStandardMaterial({
    color: 0x4040ff,
    roughness: 0.2,
    metalness: 0.8,
    wireframe: false,
  });
  
  const mesh = new THREE.Mesh(geo, mat);
  scene.add(mesh);
  
  // 动画中变形
  function deformSphere(time) {
    for (let i = 0; i < posAttr.count; i++) {
      const x = originalPos[i * 3];
      const y = originalPos[i * 3 + 1];
      const z = originalPos[i * 3 + 2];
      
      const n = Math.sin(x * 2 + time) * Math.cos(y * 2 + time * 0.7) * 0.15;
      const len = Math.sqrt(x*x + y*y + z*z);
      
      posAttr.array[i * 3]     = x + (x/len) * n;
      posAttr.array[i * 3 + 1] = y + (y/len) * n;
      posAttr.array[i * 3 + 2] = z + (z/len) * n;
    }
    posAttr.needsUpdate = true;
    geo.computeVertexNormals();
  }
  
  return { mesh, deformSphere };
}
```

## 模式3：着色器平面（GLSL 视觉效果）

```javascript
function createShaderPlane(scene) {
  const geo = new THREE.PlaneGeometry(4, 4, 32, 32);
  
  const mat = new THREE.ShaderMaterial({
    uniforms: {
      uTime: { value: 0 },
      uMouse: { value: new THREE.Vector2(0, 0) },
      uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
    },
    vertexShader: `
      varying vec2 vUv;
      varying vec3 vPosition;
      uniform float uTime;
      
      void main() {
        vUv = uv;
        vPosition = position;
        
        vec3 pos = position;
        pos.z = sin(pos.x * 3.0 + uTime) * cos(pos.y * 3.0 + uTime * 0.8) * 0.3;
        
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `,
    fragmentShader: `
      varying vec2 vUv;
      varying vec3 vPosition;
      uniform float uTime;
      uniform vec2 uMouse;
      
      void main() {
        vec2 uv = vUv;
        
        // 距离鼠标的光晕效果
        float dist = distance(uv, uMouse * 0.5 + 0.5);
        float glow = smoothstep(0.5, 0.0, dist) * 0.5;
        
        // 渐变色
        vec3 color1 = vec3(0.1, 0.0, 0.4);
        vec3 color2 = vec3(0.8, 0.2, 0.0);
        vec3 color = mix(color1, color2, uv.x + sin(uTime * 0.5) * 0.2);
        
        gl_FragColor = vec4(color + glow, 1.0);
      }
    `,
    side: THREE.DoubleSide,
  });
  
  const mesh = new THREE.Mesh(geo, mat);
  scene.add(mesh);
  return { mesh, mat };
}
```

## 完整 Three.js 初始化

```javascript
function initWebGL(canvas) {
  const W = window.innerWidth;
  const H = window.innerHeight;
  
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance',
  });
  renderer.setSize(W, H);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));  // 限制最大2x
  
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, W / H, 0.1, 100);
  camera.position.z = 3;
  
  // 光照
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  const pointLight = new THREE.PointLight(0xffffff, 1);
  pointLight.position.set(2, 3, 4);
  scene.add(ambientLight, pointLight);
  
  // 响应式
  window.addEventListener('resize', () => {
    const W = window.innerWidth, H = window.innerHeight;
    renderer.setSize(W, H);
    camera.aspect = W / H;
    camera.updateProjectionMatrix();
  });
  
  return { scene, camera, renderer };
}
```
