'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Form';
import { cn } from '@/lib/utils';

interface Member {
  id: string;
  name: string;
  email: string;
  phone: string;
  status: 'active' | 'inactive';
}

interface MemberAssignmentProps {
  groupId: string;
  groupName: string;
  onClose: () => void;
  className?: string;
}

export default function MemberAssignment({
  groupId,
  groupName,
  onClose,
  className,
}: MemberAssignmentProps) {
  const [members, setMembers] = useState<Member[]>([]);
  const [selectedMembers, setSelectedMembers] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // TODO: Replace with actual API call
    const fetchMembers = async () => {
      try {
        // Mock data for now
        const mockMembers: Member[] = [
          {
            id: '1',
            name: 'John Doe',
            email: 'john@example.com',
            phone: '+1 (555) 123-4567',
            status: 'active',
          },
          {
            id: '2',
            name: 'Jane Smith',
            email: 'jane@example.com',
            phone: '+1 (555) 234-5678',
            status: 'active',
          },
          {
            id: '3',
            name: 'Bob Johnson',
            email: 'bob@example.com',
            phone: '+1 (555) 345-6789',
            status: 'inactive',
          },
        ];
        setMembers(mockMembers);
      } catch (error) {
        console.error('Error fetching members:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMembers();
  }, []);

  const filteredMembers = members.filter(
    (member) =>
      member.status === 'active' &&
      (member.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        member.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
        member.phone.includes(searchQuery))
  );

  const handleToggleMember = (memberId: string) => {
    setSelectedMembers((prev) =>
      prev.includes(memberId)
        ? prev.filter((id) => id !== memberId)
        : [...prev, memberId]
    );
  };

  const handleSubmit = async () => {
    try {
      // TODO: Replace with actual API call
      console.log('Assigning members to group:', {
        groupId,
        memberIds: selectedMembers,
      });
      onClose();
    } catch (error) {
      console.error('Error assigning members:', error);
    }
  };

  return (
    <div className={cn('space-y-6', className)}>
      <div>
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
          Assign Members to {groupName}
        </h2>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Select members to add to this group
        </p>
      </div>

      <div>
        <Input
          type="search"
          placeholder="Search members..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="mb-4"
        />

        <div className="max-h-96 overflow-y-auto rounded-md border border-gray-200 dark:border-gray-700">
          {isLoading ? (
            <div className="p-4 text-center text-gray-500 dark:text-gray-400">
              Loading members...
            </div>
          ) : filteredMembers.length === 0 ? (
            <div className="p-4 text-center text-gray-500 dark:text-gray-400">
              No members found
            </div>
          ) : (
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {filteredMembers.map((member) => (
                <label
                  key={member.id}
                  className="flex cursor-pointer items-center p-4 hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  <input
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary dark:border-gray-600"
                    checked={selectedMembers.includes(member.id)}
                    onChange={() => handleToggleMember(member.id)}
                  />
                  <div className="ml-3">
                    <div className="font-medium text-gray-900 dark:text-white">
                      {member.name}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      {member.email} • {member.phone}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="flex justify-end gap-4">
        <Button type="button" variant="outline" onClick={onClose}>
          Cancel
        </Button>
        <Button
          type="button"
          onClick={handleSubmit}
          disabled={selectedMembers.length === 0}
        >
          Assign {selectedMembers.length} Member
          {selectedMembers.length !== 1 ? 's' : ''}
        </Button>
      </div>
    </div>
  );
} 