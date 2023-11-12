'use client';
import React from 'react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

// Define the props type
interface DownloadFilesProps {
  componentId: string;
}

const DownloadFiles: React.FC<DownloadFilesProps> = ({ componentId }) => {
  const getComponentElement = (): HTMLElement | null => document.getElementById(componentId);

  const downloadPDF = async () => {
    const element = getComponentElement();
    if (element) {
      const canvas = await html2canvas(element);
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'px',
        format: [canvas.width, canvas.height]
      });
      // Adding the image; adjust x, y, width, height as necessary
      pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
      pdf.save('combo-chart.pdf');
    }
  };
  

  const downloadPNG = async () => {
    const element = getComponentElement();
    if (element) {
      const canvas = await html2canvas(element);
      const imgData = canvas.toDataURL('image/png');
      const a = document.createElement('a');
      a.href = imgData;
      a.download = 'combo-chart.png';
      a.click();
    }
  };

  return (
    <div>
      <button onClick={downloadPDF}>Download as PDF</button>
      <button onClick={downloadPNG}>Download as PNG</button>
    </div>
  );
};

export default DownloadFiles;

