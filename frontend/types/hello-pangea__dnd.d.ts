declare module '@hello-pangea/dnd' {
  export interface DropResult {
    draggableId: string;
    type: string;
    source: {
      droppableId: string;
      index: number;
    };
    destination: {
      droppableId: string;
      index: number;
    } | null;
    reason: 'DROP' | 'CANCEL';
  }

  export interface DroppableProvided {
    innerRef: (element: HTMLElement | null) => void;
    placeholder?: React.ReactNode;
    droppableProps: {
      [key: string]: any;
    };
  }

  export interface DraggableProvided {
    innerRef: (element: HTMLElement | null) => void;
    draggableProps: {
      [key: string]: any;
    };
    dragHandleProps: {
      [key: string]: any;
    };
  }

  export interface DragDropContextProps {
    onDragEnd: (result: DropResult) => void;
    children: React.ReactNode;
  }

  export interface DroppableProps {
    droppableId: string;
    children: (provided: DroppableProvided) => React.ReactNode;
  }

  export interface DraggableProps {
    draggableId: string;
    index: number;
    children: (provided: DraggableProvided) => React.ReactNode;
  }

  export class DragDropContext extends React.Component<DragDropContextProps> {}
  export class Droppable extends React.Component<DroppableProps> {}
  export class Draggable extends React.Component<DraggableProps> {}
} 