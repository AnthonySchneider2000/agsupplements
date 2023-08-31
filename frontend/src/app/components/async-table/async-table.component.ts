// table.component.ts
import { Component, OnInit, ViewChild } from '@angular/core';
import { DataService } from '../../services/data.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-async-table',
  templateUrl: './async-table.component.html',
  styleUrls: ['./async-table.component.css'],
})
export class AsyncTableComponent implements OnInit {
  dataSource: MatTableDataSource<any>;
  displayedColumns: string[] = ['column1', 'column2', 'column3'];
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.fetchData().subscribe((data) => {
      this.dataSource = new MatTableDataSource(data);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      console.log("In component:");
      console.log(this.dataSource);
      console.log(this.displayedColumns);
    });
  }
}
