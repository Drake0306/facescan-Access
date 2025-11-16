import MainLayout from '@/components/layout/MainLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'

export default function VisitorsPage() {
  return (
    <MainLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Visitors</h1>
            <p className="text-muted-foreground">Manage registered visitors and their details</p>
          </div>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Add Visitor
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Visitor List</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center text-muted-foreground py-8">
              No visitors registered yet
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
