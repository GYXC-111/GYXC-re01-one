import React, { useRef, useEffect } from 'react';
import { fabric } from 'fabric';
import { Editor, Toolbar } from '@toast-ui/react-editor';
import '@toast-ui/editor/dist/toastui-editor.css';

const ImageEditor = ({ template, onSave }) => {
  const canvasRef = useRef(null);
  const fabricCanvas = useRef(null);

  useEffect(() => {
    fabricCanvas.current = new fabric.Canvas(canvasRef.current, {
      width: 800,
      height: 600,
      backgroundColor: '#fff'
    });
    // 加载模板背景图
    fabric.Image.fromURL(template.background, img => {
      img.scaleToWidth(800).set({ selectable: false });
      fabricCanvas.current.add(img);
    });
  }, [template]);

  const addText = () => {
    const text = new fabric.IText('输入文字', {
      left: 100,
      top: 100,
      fontSize: 24,
      fill: '#000',
      fontFamily: 'Arial'
    });
    fabricCanvas.current.add(text);
  };

  const adjustBrightness = (value) => {
    fabricCanvas.current.forEachObject(obj => {
      if (obj.type === 'image') {
        obj.filters[0] = new fabric.Image.filters.Brightness({ brightness: value / 100 });
        obj.applyFilters();
      }
    });
    fabricCanvas.current.renderAll();
  };

  const handleSave = () => {
    fabricCanvas.current.toDataURL({ format: 'png' }, (dataURL) => {
      onSave(dataURL);
    });
  };

  return (
    <div className="editor-container">
      <div className="tools-bar">
        <button onClick={addText} className="btn btn-primary">添加文字</button>
        <input type="range" min="-100" max="100" onChange={(e) => adjustBrightness(e.target.value)} />
      </div>
      <canvas ref={canvasRef} id="editorCanvas" />
      <button onClick={handleSave} className="btn btn-success mt-3">保存排版</button>
    </div>
  );
};

export default ImageEditor;
    