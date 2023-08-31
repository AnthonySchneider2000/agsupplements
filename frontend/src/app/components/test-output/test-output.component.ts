import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-test-output',
  templateUrl: './test-output.component.html',
  styleUrls: ['./test-output.component.css']
})
export class TestOutputComponent {
  backendData: any;

  constructor(private http: HttpClient) {}

  fetchData() {
    const backendUrl = 'http://localhost:8000/backend/get-dummy-data/';

    this.http.get(backendUrl).subscribe({
      next: (response) => {
        this.backendData = response;
      },
      error: (error) => {
        console.error('Error fetching data:', error);
      }
    });
  }

  formatAsJson(data: any): string {
    return JSON.stringify(data, null, 2);
  }
}
