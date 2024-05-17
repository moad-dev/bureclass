<script setup>
    defineProps(['title'])
</script>

<template>
    <div class="container-auth">
        <h1>{{ title }}</h1>
        <div class="card">
            <slot></slot>
        </div>
    </div>
</template>

<style scoped>
  .container-auth
  {
      margin: 208px 0;
      display: grid;
      align-content: center;
      justify-items: center;
  }
  .card
  {
      padding: 30px 10px;
      display: grid;
      border: 1px solid var(--vt-c-divider-light-2);
  }
  h1
  {
      text-align: center;
      margin-bottom: 20px;
      color: var(--vt-c-black-soft);
  }
</style>