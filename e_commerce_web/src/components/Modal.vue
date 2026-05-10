<template>
  <teleport to="body">
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content" :style="{ maxWidth: width }">
        <div class="modal-header">
          <h3>{{ title }}</h3>
          <button class="btn btn-icon btn-secondary" @click="$emit('close')">&#10005;</button>
        </div>
        <div class="modal-body">
          <slot />
        </div>
        <div class="modal-footer" v-if="$slots.footer">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
defineProps({
  title: { type: String, default: '' },
  width: { type: String, default: '520px' }
})
defineEmits(['close'])
</script>
