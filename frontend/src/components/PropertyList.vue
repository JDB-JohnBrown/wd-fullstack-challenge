<template>
    <v-container>
      <h1>Property Management UI</h1>
      <p>This UI developed to handle Property Management.</p>
      <v-row>
        <v-col sm="12">
          <v-alert v-if="responseSuccess" dense text type="success">
            You have successfully added property.
          </v-alert>
        </v-col>
        <v-col sm="6">
          <h3>Add Property</h3>
          <v-text-field
            v-model="memberRegistration.firstName"
            label="First name"
          ></v-text-field>
          <v-text-field
            v-model="memberRegistration.lastName"
            label="Last name"
          ></v-text-field>
          <v-btn color="primary" v-on:click="createMember">
            Register
          </v-btn>
        </v-col>
        <v-col sm="6">
          <h3>Registered Properties</h3>
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    Full Address
                  </th>
                  <th class="text-left">
                    Class Description
                  </th>
                  <th class="text-left">
                    Estimated Market Value
                  </th>
                  <th class="text-left">
                    Delete?
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="property in registeredProperties" :key="property.property_id">
                  <td>{{ property.full_address }}</td>
                  <td>{{ property.class_description }}</td>
                  <td>{{ property.estimated_market_value }}</td>
                  <td>
                    <v-btn
                        rounded
                        color="primary"                        
                        v-on:click="deletePLink(property.property_id)"                        
                        >Delete</v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
      </v-row>
    </v-container>
  </template>
  <script>
  import apiClient from "@/modules/property/propInterface";
  export default {
    name: "Member",
    data() {
      return {
        memberRegistration: {
        firstName: "",
        lastName: "",
      },
        registeredProperties: [],
        responseSuccess: false,
      };
    },
    methods: {  
      readProperties: async function() {
        const data = await apiClient.readUserProperties()
        console.log(data);
        this.registeredProperties = data;
      }, 
      deletePLink: async function(p_id){
        console.log(p_id);
      }
    },
    mounted() {
      this.readProperties();
    }
  };
  </script>