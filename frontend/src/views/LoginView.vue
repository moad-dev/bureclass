<script setup>
import AuthComponent from "../components/AuthComponent.vue";
</script>

<template>
    <AuthComponent title="Вход">
        <form id="form" @submit="onSubmit">
            <input class="card-item" name="login"  type="text" v-model="loginForm.login" required placeholder="Email">
            <input class="card-item" name="password" type="password" v-model="loginForm.password" required placeholder="Пароль">
            <button class="card-item submit-button">Войти</button>
        </form>
        <p>{{ message }}</p>
    </AuthComponent>
</template>

<script>
    import axios from "axios";

    export default {
        data() {
            return {
                loginForm: {
                    login: '',
                    password: '',
                },
                message: ''
            }
        },
        methods: {
            login(user){
                new Promise ((resolve, reject) => {
                    axios.post("/api/auth/login", user)
                        .then(resp => {
                            const token = resp.data.data.token;
                            const name = resp.data.data.name
                            localStorage.setItem('user-token', token) // store the token in localstorage
                            localStorage.setItem('user-name', name)

                            window.dispatchEvent(new CustomEvent('token-changed', {
                                detail: {
                                    storage: localStorage.getItem('user-token'),
                                    name: localStorage.getItem('user-name')
                                }
                            }));

                            resolve(resp)
                        })
                        .catch((error) => {
                            this.message = error.response.data.error;
                            localStorage.removeItem('user-token') // if the request fails, remove any possible user token if possible
                            reject(error)
                        });
                }).then(() => {
                    this.$router.push('/');
                })
            },
            initForm() {
                this.loginForm.login = '';
                this.loginForm.password = '';
            },
            onSubmit(evt) {
                evt.preventDefault();
                const payload = {
                    email: this.loginForm.login,
                    password: this.loginForm.password,
                };
                this.login(payload);
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