<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <header>
        <div class="header-bar">
            <img src="./assets/logo_true.png" width="75"  alt="logo">
            <nav>
                <RouterLink to="/" class="nav-item">Главная</RouterLink>
                <RouterLink to="/materials" class="nav-item">Материалы</RouterLink>
            </nav>
        </div>
    </header>

    <div class="container">
        <RouterView />
    </div>
</template>

<script>

</script>

<style scoped>
    .header-bar
    {
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0 auto;
        max-width: var(--vp-screen-max-width);
    }
    .container
    {
        margin: 0 auto;
        max-width: var(--vp-screen-max-width);
    }
    header
    {
        display: flex;
        border-bottom: 1px solid var(--vt-c-divider-light-2);
        padding: 0 32px;
        height: var(--vt-nav-height);
        align-items: center;
    }
    nav
    {
        display: flex;
    }
    .nav-item
    {
        padding: 12px;
    }
    .auth-container
    {
        display: flex;
    }
    .logout
    {
        cursor: pointer;
    }
</style>
