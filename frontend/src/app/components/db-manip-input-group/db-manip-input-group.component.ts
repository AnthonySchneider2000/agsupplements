import { Component } from '@angular/core';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-db-manip-input-group',
  templateUrl: './db-manip-input-group.component.html',
  styleUrls: ['./db-manip-input-group.component.css']
})
export class DbManipInputGroupComponent {
  name: string = '';
  description: string = '';
  price: number = 0;
  id: number = 0;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
  }


  handleAddDataToDatabase() {
    if(this.name) {
      this.dataService.addDataToDatabase(this.name, this.description, this.price);
    }else{
      console.log("No name provided");
    }
  }

  handleDeleteDataFromDatabase() {
    if(this.id) {
      this.dataService.deleteDataFromDatabase(this.id);
    }else{
      console.log("No id provided");
    }
  }


}
