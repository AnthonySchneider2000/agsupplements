import { Component } from '@angular/core';
import { DataService } from 'src/app/services/data.service';
import { ItemWithIngredients as Item } from 'src/app/services/models.service';

@Component({
  selector: 'app-product-page',
  templateUrl: './product-page.component.html',
  styleUrls: ['./product-page.component.css']
})
export class ProductPageComponent {
  item: Item = {
    id: 0,
    name: '',
    description: '',
    price: 0,
    link: '',
    servings: 0,
    ingredients: [],
  };


  constructor(
    private dataService: DataService,
  ) {
    // load id from local storage
    this.item.id = parseInt(localStorage.getItem('selectedId') || '0');
    // load item from database
    if(this.item.id != 0) {
      this.getItemData();
    }
  }

  getItemData() {
    this.dataService.fetchItemById(this.item.id).subscribe((item) => {
      this.item = item;
    });
  }
  


}
