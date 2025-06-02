<template>
    <div class="signature-container">
      <canvas
        ref="canvasRef"
        :width="width"
        :height="height"
        class="signature-canvas"
        @mousedown="startDrawing"
        @mousemove="draw"
        @mouseup="stopDrawing"
        @mouseleave="stopDrawing"
        @touchstart.prevent="startDrawing"
        @touchmove.prevent="draw"
        @touchend.prevent="stopDrawing"
      ></canvas>
      <button type="button" @click="clearCanvas">Clear</button>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted, defineProps, defineEmits } from 'vue';
  
  const props = defineProps({
    modelValue: String,
    width: {
      type: Number,
      default: 400,
    },
    height: {
      type: Number,
      default: 200,
    }
  });
  const emit = defineEmits(['update:modelValue']);
  
  const canvasRef = ref(null);
  const isDrawing = ref(false);
  let ctx = null;
  
  const getCanvasPos = (e) => {
    const canvas = canvasRef.value;
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return {
      x: clientX - rect.left,
      y: clientY - rect.top,
    };
  };
  
  const startDrawing = (e) => {
    isDrawing.value = true;
    const { x, y } = getCanvasPos(e);
    ctx.beginPath();
    ctx.moveTo(x, y);
  };
  
  const draw = (e) => {
    if (!isDrawing.value) return;
    const { x, y } = getCanvasPos(e);
    ctx.lineTo(x, y);
    ctx.stroke();
  };
  
  const stopDrawing = () => {
    if (!isDrawing.value) return;
    isDrawing.value = false;
    emit('update:modelValue', canvasRef.value.toDataURL());
  };
  
  const clearCanvas = () => {
    ctx.clearRect(0, 0, props.width, props.height);
    emit('update:modelValue', '');
  };
  
  onMounted(() => {
    const canvas = canvasRef.value;
    ctx = canvas.getContext('2d');
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
  
    if (props.modelValue) {
      const img = new Image();
      img.onload = () => {
        ctx.drawImage(img, 0, 0);
      };
      img.src = props.modelValue;
    }
  });
  </script>
  
  <style scoped>
  .signature-container {
    display: flex;
    flex-direction: column;
    align-items: start;
  }
  
  .signature-canvas {
    border: 1px solid #ccc;
    touch-action: none;
    cursor: crosshair;
  }
  </style>
  