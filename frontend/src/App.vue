<template>
  <div>
    <h1>Data from API:</h1>
    <ul>
      <li v-for="item in items" :key="item.id">{{ item.name }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      items: [],
    };
  },
  mounted() {
    // Use the API endpoint URL from your backend app's URL configuration
    const endpointUrl = 'http://localhost:8000/backend/get-data/';

    axios.get(endpointUrl)
      .then(response => {
        this.items = response.data;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  },
};
</script>
