declare module 'jspdf' {
  interface jsPDF {
    (options?: any): jsPDF;
    splitTextToSize(text: string, fontSize: number): string[];
    save(filename: string): void;
    text(text: string, x: number, y: number, options?: any): void;
    setFontSize(size: number): void;
    setFont(fontName: string, fontStyle?: string): void;
    addPage(): void;
  }
  
  export default jsPDF;
}
