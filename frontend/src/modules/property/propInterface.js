// frontend\src\modules\property\propInterface.js
import axiosInstance from '@/plugins/connectionBuilder.js'

const apiClient = {
    async readUserProperties(){
        const response = await axiosInstance.get('/getUserListings');
        return response.data;
    }
};

export default apiClient;