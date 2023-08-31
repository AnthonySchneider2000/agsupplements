import { AfterViewInit, Component, Input, ViewChild } from '@angular/core';
import { MatTable } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { TableDataSource, TableItem, BackendData } from './table-datasource';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.css'],
})
export class TableComponent implements AfterViewInit {
  @Input() useDefaultData: boolean;
  constructor(private http: HttpClient) {}
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  // table item OR backend data
  @ViewChild(MatTable) table!:  MatTable<TableItem | BackendData>;
  dataSource: TableDataSource;

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['id', 'name'];

  ngOnInit(): void {
    console.log('useDefaultData:', this.useDefaultData);
    this.dataSource = new TableDataSource(this.http, this.useDefaultData);
    console.log('dataSource:', this.dataSource);
  }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
    this.table.dataSource = this.dataSource;
  }
}
