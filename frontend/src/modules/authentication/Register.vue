<!-- 
frontend\src\modules\authentication\Register.vue
Heavily borrowed from: https://medium.com/@andrelbaldo/register-login-and-logout-boilerplate-written-in-vue-js-and-python-as-api-5ce57e33774b
Added custom password and Username validation 
Got rid of all "email" logic, we're using usernames -->
<template>
    <v-card>
      <v-card-title primary-title>
        <h1>Register</h1>
      </v-card-title>
      <v-card-text>
        <v-form rounded v-model="isRegisterFormValid">
          <v-text-field
            name="username"
            label="Username*"
            id="username"
            v-model="username"
            prepend-icon="mdi-account-circle"
            required
            :rules="[checkIsRequired, validateUsername]"
            type="input"
          ></v-text-field>
  
          <v-text-field
            name="password"
            label="Password*"
            class="multi-line"
            id="password"
            v-model="password"
            :type="getPasswordFieldType()"
            prepend-icon="mdi-lock"
            :append-icon="getShowPasswordApendIcon()"
            @click:append="toggleShowPassword()"
            counter="50"
            required
            :rules="[checkIsRequired(password), checkMinLength(password.length,8), validatePassword(password)]"
          >
            <template v-slot:progress>
              <v-progress-linear :value="progress(8)" :color="color(8)" absolute height="7"></v-progress-linear>
            </template>
          </v-text-field>
  
          <div class="text-center">
            <v-progress-circular indeterminate color="primary" v-if="isProcessing"></v-progress-circular>
          </div>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <router-link to="login">Go to login</router-link>
        <v-spacer></v-spacer>
        <v-btn
          color="success"
          :disabled="!isRegisterFormValid || isProcessing || GetIsSnackbarVisible"
          @click="registerNewUser({username:username, password:password})"
        >
          <v-icon left>mdi-account-plus</v-icon>Register
        </v-btn>
        <SnackNotification
          v-bind:visibility="GetIsSnackbarVisible"
          v-bind:colorCondition="getIsRegistrationProcessSucceed"
          v-bind:message="getRegistrationProcessMessage"
        />
      </v-card-actions>
    </v-card>
  </template>
  
  <script>
  import { mapActions, mapGetters } from "vuex";
  import SnackNotification from "@/modules/notification/SnackNotification.vue";
  export default {
    name: "Register",
    data: function() {
      return {
        showPassword: false,
        isRegisterFormValid: false,
        username: "",
        password: ""
      };
    },
    methods: {
      getPasswordFieldType: function() {
        if (this.showPassword) {
          return "text";
        } else {
          return "password";
        }
      },
      toggleShowPassword: function() {
        this.showPassword = !this.showPassword;
      },
      getShowPasswordApendIcon: function() {
        if (this.showPassword) {
          return "mdi-eye";
        } else {
          return "mdi-eye-off";
        }
      },
      checkIsRequired: function(value, errorMessage) {
        if (!errorMessage) {
          errorMessage = "This field is required";
        }
        return !!value || errorMessage;
      },
      checkMinLength(valueLenght, minLength, errorMessage) {
        if (!errorMessage) {
          errorMessage = `Min length is ${minLength}`;
        }
        return (!!valueLenght && valueLenght >= minLength) || errorMessage;
      },
      progress(minLength) {
        return Math.min(100, (this.password.length / minLength) * 100);
      },
      color(minLength) {
        let selectedColorIndex = 0;
        if (this.progress(minLength) < 40) {
          selectedColorIndex = 0;
        } else if (
          this.progress(minLength) > 40 &&
          this.progress(minLength) < 100
        ) {
          selectedColorIndex = 1;
        } else {
          selectedColorIndex = 2;
        }
        return ["error", "warning", "success"][selectedColorIndex];
      },
      ...mapActions(["registerNewUser", "setSnackbarVisibility"]),
      validatePassword(password){
        let bool = true;
        let err = "";
        let newline = `
        `;

        if(!password.match(/\d/gm)){
            bool = false;
            if (err.length){err += newline}
            err += "Password must contain atleast one number"
        }
        if(!password.match(/[A-Z]/gm)){
            bool = false;
            if (err.length){err += newline}
            err += "Password must contain atleast one uppercase character"
        }
        if(!password.match(/[a-z]/gm)){
            bool = false;
            if (err.length){err += newline}
            err += "Password must contain atleast one lowercase character"
        }
        if(!password.match(/[$#@!*]/gm)){
            bool = false;
            if (err.length){err += newline}
            err += "Password must contain atleast one of these special characters: $#@!*"
        }
        return (bool || err);
      },
      validateUsername(username) {
        return (
            username.length >= 4 ||
            "Username needs to be atleast four characters"
        );
    }
    },
    computed: {
      ...mapGetters([
        "getIsRegistrationProcessSucceed",
        "getRegistrationProcessMessage",
        "isProcessing",
        "GetIsSnackbarVisible"
      ])
    },
    components: {
      SnackNotification
    }
  };
  </script>
  <style>
    .multi-line {
      white-space: pre-line;
    }
  </style>