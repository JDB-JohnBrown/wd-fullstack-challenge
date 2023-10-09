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
          <h3>Search Property</h3>          
          <v-text-field
            v-model="searchBox.address"
            label="Address"
          ></v-text-field>
          <v-text-field
            v-model="searchBox.class_d"
            label="Description"
          ></v-text-field>
          <v-text-field
            v-model="searchBox.val"
            label="Estimated Market Value"
          ></v-text-field>
          <v-text-field
            v-model="searchBox.use"
            label="Building Use"
          ></v-text-field>
          <v-text-field
            v-model="searchBox.sqft"
            label="Sq. Ft"
          ></v-text-field>
          <v-btn color="primary" v-on:click="updateSearch">
            Search
          </v-btn>
          <v-data-table
                v-model:page="searchPage"
                :headers="searchHeaders"
                :items="searchedProperties"
                :items-per-page="itemsPerPage"
                class="elevation-1"
            >
                <template v-slot:item="row">
                    <tr>
                        <td>{{row.item.full_address}}</td>
                        <td>{{row.item.class_description}}</td>
                        <td>{{row.item.estimated_market_value}}</td>
                        <td>{{row.item.bldg_use}}</td>
                        <td>{{row.item.building_sq_ft}}</td>
                        <td>
                            <v-btn density="compact" size="small" dark color="green" :disabled="row.item.exists" @click="addPLink(row.item.property_id)">
                                <v-icon tiny dark>mdi-plus</v-icon>
                            </v-btn>
                        </td>
                    </tr>
                </template>
  </v-data-table>
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
        searchBox: {
            address:"", 
            class_d:"", 
            val:"", 
            use:"", 
            sqft:""
        },
        registeredProperties: [],
        responseSuccess: false,
        searchPage: 1,
        itemsPerPage: 5,
        searchHeaders: [
          {
            align: 'start',
            value: 'full_address',            
            text: 'Full Address',
          },
          { text: 'Class Description', value: 'class_description' },
          { text: 'Estimated Market Value', value: 'estimated_market_value' },
          { text: 'Buidling Use', value: 'bldg_use' },
          { text: 'Building SQ Ft', value: 'building_sq_ft' },
          { text: 'Add?', value: 'add', sortable: false,},
        ],
        searchedProperties: []
      };
    },
    methods: {  
      readProperties: async function() {
        const data = await apiClient.readUserProperties()
        console.log(data);
        this.registeredProperties = data;
      }, 
      deletePLink: async function(p_id){
        const data = await apiClient.deleteUserProperty(p_id)
        console.log(data);
        this.readProperties();
      },
      addPLink: async function(p_id){
        const data = await apiClient.addUserProperty(p_id)
        console.log(data);
        this.readProperties();
      },
      updateSearch: async function(){
        const data = await apiClient.searchProperties(this.searchBox)
        console.log(data);
        var _this = this;
        data.forEach(function (i){
            i.exists = _this.registeredProperties.some(function(element) {
                return element.property_id == i.property_id;
            });
        });
        this.searchedProperties = data;
      }
    },
    mounted() {
      this.readProperties();
    },
    computed: {
      pageCount () {
        return Math.ceil(this.searchedProperties.length / this.itemsPerPage)
      },
    },
  };
  </script>
  <style>
    .theme--dark.v-btn.v-btn--disabled.v-btn--has-bg {
    background-color: gray !important;
    }
</style>