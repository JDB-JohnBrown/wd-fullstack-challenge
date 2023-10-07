<!-- 
frontend\src\modules\authentication\Login.vue
Author: Author : Andre Baldo (http://github.com/andrebaldo/) -->
<template>
    <v-card>
      <v-card-title primary-title>
        <h1>Login</h1>
      </v-card-title>
      <v-card-text>
        <v-form rounded v-model="isLoginFormValid">
          <v-text-field
            name="username"
            label="Username*"
            id="username"
            v-model="username"
            prepend-icon="mdi-account-circle"
            required
            :rules="[checkIsRequired(username), validateUsername(username)]"
          ></v-text-field>
  
          <v-text-field
            name="password"
            label="Password*"
            id="password"
            v-model="password"
            :type="getPasswordFieldType()"
            prepend-icon="mdi-lock"
            :append-icon="getShowPasswordApendIcon()"
            @click:append="toggleShowPassword()"
            required
          ></v-text-field>
  
          <div class="text-center">
            <v-progress-circular indeterminate color="primary" v-if="isProcessing"></v-progress-circular>
          </div>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <router-link to="register">Go to Register</router-link>
        <v-spacer></v-spacer>
        <v-btn
          color="success"
          :disabled="!isLoginFormValid || isProcessing || GetIsSnackbarVisible"
          @click="login({username:username, password:password})"
        >Login</v-btn>
      </v-card-actions>
      <SnackNotification
        v-bind:visibility="GetIsSnackbarVisible"
        v-bind:colorCondition="getIsUserLoggedIn"
        v-bind:message="getLoginProcessMessage"
      />
    </v-card>
  </template>
  
  <script>
  import { mapActions, mapGetters } from "vuex";
  import SnackNotification from "@/modules/notification/SnackNotification.vue";
  export default {
    name: "Login",
    data: function() {
      return {
        showPassword: false,
        isLoginFormValid: false,
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
      ...mapActions(["authenticateUserAndSetToken"]),
      validateUsername(username) {
        return (
            username.length >= 4 ||
            "Username should be atleast four characters"
        );
      },
      login(loginData){
        loginData.controllerReference = this;
        this.authenticateUserAndSetToken(loginData)
        .then(function(controller){
          controller.$router.push('/')
        }).catch(function () {
            console.log("Promise Rejected");
        })
      }
    },
    computed: {
      ...mapGetters([
        "getLoginProcessMessage",
        "isProcessing",
        "getIsUserLoggedIn",
        "GetIsSnackbarVisible"
      ])
    },
    components: {
      SnackNotification
    }
  };
  </script>