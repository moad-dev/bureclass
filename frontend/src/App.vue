<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <header>
        <div class="header-bar">
            <img src="./assets/logo_true.svg" width="150"  alt="logo">
            <nav>
                <RouterLink to="/" class="nav-item">Главная</RouterLink>
                <RouterLink v-if="!isLoggedIn" to="/register" class="nav-item">Регистрация</RouterLink>
                <RouterLink v-if="!isLoggedIn" to="/login" class="nav-item">Войти</RouterLink>
                <RouterLink v-if="isLoggedIn" to="/analyzes" class="nav-item">Анализы</RouterLink>
                <div v-if="isLoggedIn" class="auth-container">
                    <p class="nav-item">{{ name }}</p>
                    <RouterLink to="/" @click="logout" class="nav-item logout">Выйти</RouterLink>
                </div>
            </nav>
        </div>
    </header>

    <div class="container">
        <RouterView />
    </div>
</template>

<script>
import { updateState } from "@/router";

export default
{
    mounted() {
        window.addEventListener('token-changed', (event) => {
            this.token = event.detail.storage;
            this.name = event.detail.name;
            updateState()
        });
        this.token = localStorage.getItem('user-token')
        this.name = localStorage.getItem('user-name')
    },
    data() {
        return {
            token: null,
            name: null
        }
    },
    computed: {
        isLoggedIn() {
            return !!this.token
        }
    },
    methods: {
        logout() {
            localStorage.removeItem('user-token')
            localStorage.removeItem('user-name')
            window.dispatchEvent(new CustomEvent('token-changed', {
                detail: {
                    storage: undefined,
                    name: undefined
                }
            }));
        }
    }
}
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
