import { PrismaClient } from '@prisma/client';
import { faker } from '@faker-js/faker';

const prisma = new PrismaClient();

async function seedData() {
  try {
    // Create dummy users
    const users = await Promise.all(
      Array(10).fill(null).map(async () => {
        const email = faker.internet.email();
        const password = await bcrypt.hash('password123', 10);
        
        return prisma.user.create({
          data: {
            email,
            password,
            name: faker.person.fullName(),
            role: faker.helpers.arrayElement(['USER', 'ADMIN']),
            emailVerified: new Date(),
          },
        });
      })
    );

    // Create dummy projects
    const projects = await Promise.all(
      Array(5).fill(null).map(() =>
        prisma.project.create({
          data: {
            name: faker.company.name(),
            description: faker.lorem.paragraph(),
            status: faker.helpers.arrayElement(['ACTIVE', 'COMPLETED', 'ON_HOLD']),
            startDate: faker.date.past(),
            endDate: faker.date.future(),
            budget: faker.number.int({ min: 1000, max: 100000 }),
            progress: faker.number.int({ min: 0, max: 100 }),
          },
        })
      )
    );

    // Create dummy events
    const events = await Promise.all(
      Array(8).fill(null).map(() =>
        prisma.event.create({
          data: {
            title: faker.lorem.sentence(),
            description: faker.lorem.paragraph(),
            startDate: faker.date.future(),
            endDate: faker.date.future(),
            location: faker.location.city(),
            type: faker.helpers.arrayElement(['MEETING', 'FUNDRAISER', 'VOLUNTEER']),
            status: faker.helpers.arrayElement(['SCHEDULED', 'IN_PROGRESS', 'COMPLETED']),
          },
        })
      )
    );

    // Create dummy contributions
    const contributions = await Promise.all(
      Array(20).fill(null).map(() =>
        prisma.contribution.create({
          data: {
            amount: faker.number.int({ min: 10, max: 1000 }),
            type: faker.helpers.arrayElement(['DONATION', 'MEMBERSHIP', 'SPONSORSHIP']),
            status: faker.helpers.arrayElement(['PENDING', 'COMPLETED', 'FAILED']),
            userId: faker.helpers.arrayElement(users).id,
            projectId: faker.helpers.arrayElement(projects).id,
            date: faker.date.recent(),
          },
        })
      )
    );

    // Create dummy groups
    const groups = await Promise.all(
      Array(3).fill(null).map(() =>
        prisma.group.create({
          data: {
            name: faker.company.name(),
            description: faker.lorem.paragraph(),
            type: faker.helpers.arrayElement(['COMMUNITY', 'PROFESSIONAL', 'EDUCATIONAL']),
            status: faker.helpers.arrayElement(['ACTIVE', 'INACTIVE']),
          },
        })
      )
    );

    console.log('Dummy data created successfully:');
    console.log(`- ${users.length} users`);
    console.log(`- ${projects.length} projects`);
    console.log(`- ${events.length} events`);
    console.log(`- ${contributions.length} contributions`);
    console.log(`- ${groups.length} groups`);

  } catch (error) {
    console.error('Error seeding data:', error);
  } finally {
    await prisma.$disconnect();
  }
}

seedData(); 