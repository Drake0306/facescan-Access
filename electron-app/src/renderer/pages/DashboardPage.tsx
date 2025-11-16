import { useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Camera, Users, LogIn, LogOut } from 'lucide-react'
import MainLayout from '@/components/layout/MainLayout'
import { wsService } from '@/lib/websocket'
import { useToast } from '@/components/ui/use-toast'

export default function DashboardPage() {
  const { toast } = useToast()

  useEffect(() => {
    // Connect to WebSocket
    const socket = wsService.connect()

    // Listen for face detection events
    socket?.on('face_detected', (data) => {
      toast({
        title: 'Face Detected',
        description: data.recognized ? `Welcome, ${data.visitor_name}` : 'Unknown visitor',
      })
    })

    socket?.on('gate_opened', (data) => {
      toast({
        title: 'Gate Opened',
        description: `Gate opened for ${data.visitor_name}`,
      })
    })

    return () => {
      wsService.disconnect()
    }
  }, [toast])

  return (
    <MainLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Monitor gate activity and system status</p>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Cameras</CardTitle>
              <Camera className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">2</div>
              <p className="text-xs text-muted-foreground">Entry & Exit</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Visitors</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">0</div>
              <p className="text-xs text-muted-foreground">Registered</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Today's Entries</CardTitle>
              <LogIn className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">0</div>
              <p className="text-xs text-muted-foreground">Visitors entered</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Currently Inside</CardTitle>
              <LogOut className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">0</div>
              <p className="text-xs text-muted-foreground">Active visitors</p>
            </CardContent>
          </Card>
        </div>

        {/* Live Camera Feeds */}
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Entry Camera</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
                <p className="text-muted-foreground">Camera feed will appear here</p>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Exit Camera</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
                <p className="text-muted-foreground">Camera feed will appear here</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center text-muted-foreground py-8">
              No recent activity
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
