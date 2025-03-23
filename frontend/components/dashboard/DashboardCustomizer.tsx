'use client';

import { useState, useCallback } from 'react';
import { DragDropContext, Droppable, Draggable, DropResult, DroppableProvided, DraggableProvided } from '@hello-pangea/dnd';
import { Cog6ToothIcon } from '@heroicons/react/24/outline';
import { Button } from '@/components/ui/Button';
import Card from '@/components/ui/card';
import { cn } from '@/lib/utils';

export interface WidgetConfig {
  id: string;
  title: string;
  type: string;
  size: 'small' | 'medium' | 'large';
  visible: boolean;
}

interface DashboardCustomizerProps {
  widgets: WidgetConfig[];
  onWidgetsChange: (widgets: WidgetConfig[]) => void;
}

const sizeOptions = [
  { label: 'Small', value: 'small' },
  { label: 'Medium', value: 'medium' },
  { label: 'Large', value: 'large' },
];

export function DashboardCustomizer({ widgets, onWidgetsChange }: DashboardCustomizerProps) {
  const [isOpen, setIsOpen] = useState(false);

  const handleDragEnd = useCallback(
    (result: DropResult) => {
      if (!result.destination) return;

      const items = Array.from(widgets);
      const [reorderedItem] = items.splice(result.source.index, 1);
      items.splice(result.destination.index, 0, reorderedItem);

      onWidgetsChange(items);
    },
    [widgets, onWidgetsChange]
  );

  const toggleWidgetVisibility = useCallback(
    (widgetId: string) => {
      onWidgetsChange(
        widgets.map((widget) =>
          widget.id === widgetId ? { ...widget, visible: !widget.visible } : widget
        )
      );
    },
    [widgets, onWidgetsChange]
  );

  const updateWidgetSize = useCallback(
    (widgetId: string, size: 'small' | 'medium' | 'large') => {
      onWidgetsChange(
        widgets.map((widget) =>
          widget.id === widgetId ? { ...widget, size } : widget
        )
      );
    },
    [widgets, onWidgetsChange]
  );

  return (
    <div className="relative">
      <Button
        variant="outline"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2"
      >
        <Cog6ToothIcon className="h-5 w-5" />
        <span>Customize Dashboard</span>
      </Button>

      {isOpen && (
        <Card className="absolute right-0 top-full z-50 mt-2 w-80 p-4 shadow-lg">
          <h3 className="mb-4 text-lg font-medium">Dashboard Layout</h3>
          <DragDropContext onDragEnd={handleDragEnd}>
            <Droppable droppableId="widgets">
              {(provided: DroppableProvided) => (
                <div
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                  className="space-y-4"
                >
                  {widgets.map((widget, index) => (
                    <Draggable
                      key={widget.id}
                      draggableId={widget.id}
                      index={index}
                    >
                      {(provided: DraggableProvided) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          className="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800"
                        >
                          <div className="flex items-center justify-between">
                            <label className="flex items-center space-x-2">
                              <input
                                type="checkbox"
                                checked={widget.visible}
                                onChange={() => toggleWidgetVisibility(widget.id)}
                                className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700"
                              />
                              <span className="text-sm font-medium">{widget.title}</span>
                            </label>
                            <select
                              value={widget.size}
                              onChange={(e) =>
                                updateWidgetSize(widget.id, e.target.value as 'small' | 'medium' | 'large')
                              }
                              className="rounded-md border-gray-300 text-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700"
                            >
                              {sizeOptions.map((option) => (
                                <option key={option.value} value={option.value}>
                                  {option.label}
                                </option>
                              ))}
                            </select>
                          </div>
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          </DragDropContext>
        </Card>
      )}
    </div>
  );
} 