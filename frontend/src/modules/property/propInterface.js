// frontend\src\modules\property\propInterface.js
import axiosInstance from '@/plugins/connectionBuilder.js'

const apiClient = {
    async readUserProperties(){
        const response = await axiosInstance.get('/getUserListings');
        return response.data;
    },
    async deleteUserProperty(propertyId){
        const response = await axiosInstance.post("/deleteUserListing", {property_id: propertyId});
        return response.data;
    },
    async searchProperties(searchBox){
        const response = await axiosInstance.post("/searchProperties", searchBox);
        return response.data;
    },
    async addUserProperty(propertyId){
        const response = await axiosInstance.post("/addUserListing", {property_id: propertyId});
        return response.data;
    }
};

export default apiClient;