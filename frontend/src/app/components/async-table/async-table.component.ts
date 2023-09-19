import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { DataService } from '../../services/data.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { TableDataService } from 'src/app/services/tabledata.service';

@Component({
  selector: 'app-async-table',
  templateUrl: './async-table.component.html',
  styleUrls: ['./async-table.component.css'],
})
export class AsyncTableComponent implements OnInit {
  @Input() data: string = 'ItemBase';
  dataSource: MatTableDataSource<any>;
  displayedColumns: string[] = [];
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(
    private dataService: DataService,
    private tableDataService: TableDataService
  ) {}

  ngOnInit(): void {
    this.loadData();
    this.tableDataService.reloadTable$.subscribe(() => {
      // reload table
      console.log('Reloading table');
      this.loadData();
    });
  }

  loadData() {
    if (this.data === 'ItemBase') {
    this.dataService.fetchItemBaseData().subscribe((data) => {
      this.dataSource = new MatTableDataSource(data);
      this.displayedColumns = this.getDisplayedColumns();
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
    } else if (this.data === 'ItemWithIngredients') {
      this.dataService.fetchItemWithIngredientsData().subscribe((data) => {
        console.log(data);
        this.dataSource = new MatTableDataSource(data);
        this.displayedColumns = this.getDisplayedColumns();
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
        console.log(data);
      });
    }
  }

  getDisplayedColumns(): string[] {
    if (this.dataSource) {
      return Object.keys(this.dataSource.data[0]);
    }
    return [];
  }

  applyFilter(event: any) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
  onRowClick(row: any) {
    this.tableDataService.setSelectedId(row.id);
  }
  capitalizeFirstLetter(string: string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
}
