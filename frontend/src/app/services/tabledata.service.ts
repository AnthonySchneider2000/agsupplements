import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TableDataService {
  private reloadTableSubject = new Subject<void>();

  // Observable for reloading the table
  reloadTable$ = this.reloadTableSubject.asObservable();

  // Method to trigger table reload
  reloadTable() {
    this.reloadTableSubject.next();
  }
}
