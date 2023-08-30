<template>
  <div>
    <h1>Data from API:</h1>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }} - {{ item.price }}
        <button @click="deleteItem(item.id)">Delete</button>
      </li>
    </ul>
    <div>
      <input v-model="newItem.name" placeholder="Name">
      <input v-model="newItem.description" placeholder="Description">
      <input v-model="newItem.price" placeholder="Price">
      <button @click="createItem">Create</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      items: [],
      newItem: {
        name: '',
        description: '',
        price: null,
      },
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      const endpointUrl = 'http://localhost:8000/backend/get-data/';
      axios.get(endpointUrl)
        .then(response => {
          this.items = response.data;
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
    createItem() {
      console.log('Creating item:', this.newItem);
      axios.post('http://localhost:8000/backend/create-item/', this.newItem)
        .then(response => {
          console.log('Item created:', response.data);
          this.fetchData();
        })
        .catch(error => {
          console.error('Error creating item:', error);
        });
    },
    deleteItem(id) {
      axios.delete(`http://localhost:8000/backend/delete-item/${id}/`)
        .then(response => {
          console.log('Item deleted:', response.data);
          this.fetchData();
        })
        .catch(error => {
          console.error('Error deleting item:', error);
        });
    },
  },
};
</script>
