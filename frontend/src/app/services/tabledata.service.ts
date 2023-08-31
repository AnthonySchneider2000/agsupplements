import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TableDataService {
  private reloadTableSubject = new Subject<void>();

  // Observable for reloading the table
  reloadTable$ = this.reloadTableSubject.asObservable();

  // Method to trigger table reload
  reloadTable() {
    this.reloadTableSubject.next();
  }

  private selectedIdSubject = new Subject<number>();

  // Observable for getting the selected id
  selectedId$ = this.selectedIdSubject.asObservable();

  setSelectedId(id: number) {
    this.selectedIdSubject.next(id);
  }
}
