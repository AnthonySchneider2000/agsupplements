import { Component } from '@angular/core';
import { DataService } from 'src/app/services/data.service';

@Component({
  selector: 'app-calculator-page',
  templateUrl: './calculator-page.component.html',
  styleUrls: ['./calculator-page.component.css']
})
export class CalculatorPageComponent {
  selectedItems: any[] = [];

  constructor(
  ) {
    // load id from local storage
    this.selectedItems = JSON.parse(localStorage.getItem('selectedItems') || '[]');
    console.log(this.selectedItems);
    // load item from database

  }


  

}
