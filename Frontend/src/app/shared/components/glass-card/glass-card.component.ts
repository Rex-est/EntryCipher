import { Component, Input, ElementRef, ViewChild, AfterViewInit, HostListener, OnChanges, SimpleChanges, inject, Renderer2, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { getDisplacementFilter } from '../../utils/displacement.utils';

@Component({
  selector: 'app-glass-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div #glassBox class="glass-box" [ngClass]="customClass" [style.borderRadius.px]="radius">
      <div class="content">
        <ng-content></ng-content>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
    }
    
    .glass-box {
      background: rgba(255, 255, 255, 0.2);
      box-shadow: 1px 1px 1px 0px rgba(255,255,255, 0.3) inset, 
                  -1px -1px 1px 0px rgba(255,255,255, 0.1) inset, 
                  0px 8px 32px 0px rgba(31, 38, 135, 0.07);
      transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
      width: 100%;
      height: 100%;
    }
    
    .glass-box:active {
      transform: scale(0.98);
    }

    .content {
      width: 100%;
      height: 100%;
      position: relative;
      z-index: 1;
    }
  `]
})
export class GlassCardComponent implements AfterViewInit, OnChanges {
  @ViewChild('glassBox') glassBox!: ElementRef<HTMLDivElement>;
  
  @Input() radius = 40;
  @Input() depth = 10;
  @Input() blur = 4;
  @Input() strength = 80;
  @Input() chromaticAberration = 2;
  @Input() customClass = '';
  @Input() backgroundColor = 'rgba(255, 255, 255, 0.2)';

  private renderer = inject(Renderer2);
  private platformId = inject(PLATFORM_ID);
  private isClicked = false;
  private resizeObserver?: any;

  ngOnChanges(changes: SimpleChanges): void {
    if (this.glassBox) {
      this.updateStyles();
    }
  }

  ngAfterViewInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.updateStyles();
      this.setupResizeObserver();
    }
  }

  private setupResizeObserver(): void {
    if (typeof ResizeObserver !== 'undefined') {
      this.resizeObserver = new ResizeObserver(() => {
        this.updateStyles();
      });
      this.resizeObserver.observe(this.glassBox.nativeElement);
    }
  }

  @HostListener('mousedown')
  onMouseDown(): void {
    this.isClicked = true;
    this.updateStyles();
  }

  @HostListener('mouseup')
  @HostListener('mouseleave')
  onMouseUp(): void {
    this.isClicked = false;
    this.updateStyles();
  }

  private updateStyles(): void {
    if (!isPlatformBrowser(this.platformId) || !this.glassBox) return;

    const element = this.glassBox.nativeElement;
    const rect = element.getBoundingClientRect();
    
    const actualWidth = Math.max(Math.ceil(rect.width), 50);
    const actualHeight = Math.max(Math.ceil(rect.height), 30);
    const currentDepth = this.isClicked ? this.depth * 1.5 : this.depth;

    const filterUrl = getDisplacementFilter({
      height: actualHeight,
      width: actualWidth,
      radius: this.radius,
      depth: currentDepth,
      strength: this.strength,
      chromaticAberration: this.chromaticAberration
    });

    this.renderer.setStyle(element, 'backdrop-filter', `blur(${this.blur / 2}px) url('${filterUrl}') blur(${this.blur}px) brightness(1.05) saturate(1.2)`);
    this.renderer.setStyle(element, 'background-color', this.backgroundColor);
  }
}
