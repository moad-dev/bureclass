<script setup>
import AuthComponent from "../components/AuthComponent.vue";
</script>

<template>
    <AuthComponent title="Регистрация">
        <form id="form" @submit="onSubmit">
            <input class="card-item" name="name" type="text" v-model="registerForm.name" required placeholder="Имя пользователя">
            <input class="card-item" name="login" type="text" v-model="registerForm.login" required placeholder="Email">
            <input class="card-item" name="password" type="password" v-model="registerForm.password" required placeholder="Пароль">
            <button class="card-item submit-button">Регистрация</button>
        </form>
        <p>{{ message }}</p>
    </AuthComponent>
</template>

<script>

import axios from "axios";

export default
{
    data() {
        return {
            registerForm: {
              name: '',
              login: '',
              password: ''
            },
            message: '',
        }
    },
    methods:{
        register(user){
            axios.post("/api/auth/register", user)
                .then(resp => {
                    this.$router.push('/login')
                })
                .catch((error) => {
                    this.message = error.response.data.error;
                });
        },
        initForm() {
            this.registerForm.name = '';
            this.registerForm.login = '';
            this.registerForm.password = '';
        },
        onSubmit(evt) {
            evt.preventDefault();
            const payload = {
                name: this.registerForm.name,
                email: this.registerForm.login,
                password: this.registerForm.password,
            };
            this.register(payload);
            this.initForm();
        },
    }
}
</script>

<style scoped>
form
{
    display: grid;
}
input {
  padding: 12px 12px;
}
.card-item
{
  margin: 5px 0;
}

</style>